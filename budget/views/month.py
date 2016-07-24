from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

from budget.models import Account
from budget.models import AccountBalance
from budget.models import Category
from budget.models import CategoryBalance
from budget.models import Location
from budget.models import Month
from budget.models import RecurringTransaction
from budget.models import Subcategory
from budget.models import Year
from budget.settings import template_base
from budget.views.general import add_url_to_context
from budget.views.general import base_context

from collections import namedtuple
from datetime import date
import json

@login_required
def main(request, year, month):
    context = base_context(request)
    m = Month.get_month(year, month)
    if m.monthlybalances.finalized:
        context['finalize'] = 'Re-finalize'
    else:
        context['finalize'] = 'Finalize'
    today = date.today()
    if int(year) < today.year:
        context['can_finalize'] = True
    elif int(year) == today.year and int(month) < today.month:
        context['can_finalize'] = True
    else:
        context['can_finalize'] = False
    context['month'] = month
    context['year'] = year
    context['month_id'] = m.id
    context['last_balanced'] = request.user.finances.last_balanced
    context['balances'] = m.monthlybalances
    context['recurring_transactions'] = RecurringTransaction.objects.all()
    add_json_variables_to_context(context)
    add_urls_to_context(context)
    balance = 0
    balance_pending = 0
    context['accounts'] = []
    prev_month = m.previous()
    prev_balance = 0
    for a in Account.objects.all():
        account = namedtuple('Account', ['id', 'name'])
        context['accounts'].append(account(a.id, a.name))
        balance += a.monthly_balance(m)
        balance_pending += a.monthly_balance(m, True)
        prev_balance += a.monthly_balance(prev_month, True)
    context['current_balance'] = balance
    context['pending_balance'] = balance_pending
    category_template = namedtuple('CategoryTemplate',
            ['name', 'id', 'income', 'budget', 'balance', 'remaining',
                'budget_width', 'remaining_width', 'subcategories'])
    context['income_categories'] = []
    context['mandatory_categories'] = []
    context['expense_categories'] = []
    context['investment_categories'] = []
    context['total_income'] = 0
    context['total_mandatory'] = 0
    context['total_expenses'] = 0
    context['total_investments'] = 0
    context['net_income'] = 0
    context['previous_balance'] = prev_balance
    context['budgeted_balance'] = (prev_balance +
            m.monthlybalances.budgeted_income -
            m.monthlybalances.budgeted_mandatory -
            m.monthlybalances.budgeted_expense -
            m.monthlybalances.budgeted_investments)
    for c in Category.objects.all():
        # Categories are set up such that their balance is what is _spent_ (to
        # make account balances and transactions easier), but budgets are
        # always _positive_.  That means that income categories have to have
        # their balance flipped to have it match the budget.
        subcategories = _render_subcategories(c, m)
        budget = c.monthly_budget(m)
        balance = c.monthly_balance(m)
        if c.type == 'I':
            balance *= -1
        remaining = budget - balance
        if c.type == 'I':
            context['total_income'] += balance
            context['net_income'] += balance
        elif c.type == 'M':
            context['total_mandatory'] += balance
            context['net_income'] -= balance
        elif c.type == 'E':
            context['total_expenses'] += balance
            context['net_income'] -= balance
        elif c.type == 'V':
            context['total_investments'] += balance
        else:
            raise ValueError("not sure how I got here")
        budget_width = 100*float(balance) / float(budget) if budget != 0 else 0
        if remaining < 0:
            budget_width = 100
        if budget_width > 100:
            budget_width = 100
        remaining_width = 100 - budget_width
        cat_template = category_template(
                c.name,
                c.id,
                c.type == 'I',
                budget,
                balance,
                remaining,
                budget_width,
                remaining_width,
                subcategories
                )
        if c.type == 'I':
            context['income_categories'].append(cat_template)
        elif c.type == 'M':
            context['mandatory_categories'].append(cat_template)
        elif c.type == 'E':
            context['expense_categories'].append(cat_template)
        elif c.type == 'V':
            context['investment_categories'].append(cat_template)
        else:
            raise ValueError("not sure how I got here")
    context['categories'] = (
            context['income_categories'] + context['mandatory_categories'] +
            context['expense_categories'] + context['investment_categories']
            )
    location_template = namedtuple('LocationTemplate',
            ['id', 'name', 'total_spent'])
    context['locations'] = []
    # TODO(matt): This is a lot of DB lookups, and should be pushed into an
    # AJAX request - it's not really looked at very much, and shouldn't be
    # allowed to slow down the initial page load.
    for l in Location.objects.all():
        if l.total_spent_in_month(m) > 0:
            context['locations'].append(location_template(l.id, l.name,
                    l.total_spent_in_month(m)))
    return render_to_response(template_base + 'month.html', context)


@login_required
def location(request, year=None, month=None, location_id=None):
    context = base_context(request)
    location = get_object_or_404(Location, pk=location_id)
    if month:
        m = Month.get_month(year, month)
        transaction_set = location.transaction_set_for_month(m)
    elif year:
        y = get_object_or_404(Year, year=year)
        transaction_set = location.transaction_set_for_year(y)
    else:
        transaction_set = location.transaction_set.all()
    context['transactions'] = []
    TransactionTemplate = namedtuple('TransactionTemplate',
            ['date', 'amount', 'account', 'description'])
    for t in transaction_set:
        amount = t.amount
        if not t.is_debit():
            amount = -1 * amount
        context['transactions'].append(TransactionTemplate(
                t.date,
                amount,
                t.account.name,
                t.get_description(),
                ))
    context['location_id'] = location_id
    context['name'] = location.name
    context['total_spent'] = location.transaction_total(transaction_set)
    return render_to_response(template_base + 'location.html', context)


@login_required
@transaction.atomic
def finalize_month(request, year, month):
    m = Month.get_month(year, month)
    total_income = 0
    total_investments = 0
    total_expense = 0
    final_balance = 0
    for a in Account.objects.all():
        balance = a.monthly_balance(m, recalculate=True)
        try:
            account_balance = AccountBalance.objects.get(account=a, month=m)
            account_balance.balance = balance
        except AccountBalance.DoesNotExist:
            account_balance = AccountBalance(account=a, month=m,
                    balance=balance)
        account_balance.save()
        final_balance += balance
    for c in Subcategory.objects.all():
        balance = c.monthly_balance(m)
        try:
            cat_balance = CategoryBalance.objects.get(subcategory=c, month=m)
            cat_balance.amount = balance
        except CategoryBalance.DoesNotExist:
            cat_balance = CategoryBalance(subcategory=c, month=m,
                    amount=balance)
        cat_balance.save()
        if c.category.type == 'I':
            total_income -= balance
        elif c.category.type == 'E':
            total_expense += balance
        elif c.category.type == 'V':
            total_investments += balance
    balances = m.monthlybalances
    balances.total_income = total_income
    balances.total_investments = total_investments
    balances.total_expense = total_expense
    balances.final_balance = final_balance
    balances.finalized = True
    balances.save()
    redirect = reverse('budget-month', kwargs={'year': year, 'month': month})
    return HttpResponseRedirect(redirect)


def _render_subcategories(category, month):
    """Return a set of subcategories suitable for rendering"""
    subcat_template = namedtuple('SubcatTemplate',
            ['name', 'id', 'budget', 'balance', 'remaining', 'budget_width',
                'remaining_width'])
    subcategories = []
    for subcat in category.subcategory_set.all():
        budget = subcat.monthly_budget(month)
        balance = subcat.monthly_balance(month)
        if category.type == 'I':
            balance *= -1
        remaining = budget - balance
        budget_width = 100*float(balance) / float(budget) if budget != 0 else 0
        if remaining < 0:
            budget_width = 100
        if budget_width > 100:
            budget_width = 100
        remaining_width = 100 - budget_width
        subcategories.append(subcat_template(
                subcat.name,
                subcat.id,
                budget,
                balance,
                remaining,
                budget_width,
                remaining_width,
                ))
    return subcategories


def add_json_variables_to_context(context):
    context['account_names_json'] = mark_safe(
            json.dumps([a.name for a in Account.objects.all()]))
    context['location_names_json'] = mark_safe(
            json.dumps([l.name for l in Location.objects.all()]))
    context['subcat_names_json'] = mark_safe(
            json.dumps([s.name for s in Subcategory.objects.all()]))


def add_urls_to_context(context):
    add_url_to_context(context, 'edit_budget',
            reverse('budget-ajax-edit-budget'))
    add_url_to_context(context, 'month_account',
            reverse('budget-ajax-month-account'))
    add_url_to_context(context, 'update_pending',
            reverse('budget-ajax-update-pending'))
    add_url_to_context(context, 'edit_transaction_date',
            reverse('budget-ajax-edit-transaction-date'))
    add_url_to_context(context, 'edit_transaction_location',
            reverse('budget-ajax-edit-transaction-location'))
    add_url_to_context(context, 'get_location_selector',
            reverse('budget-ajax-get-location-selector'))
    add_url_to_context(context, 'add_location',
            reverse('budget-ajax-add-location'))
    add_url_to_context(context, 'add_transaction',
            reverse('budget-ajax-add-transaction'))
    add_url_to_context(context, 'add_transaction_form',
            reverse('budget-ajax-add-transaction-form'))
    add_url_to_context(context, 'subcategory_transactions',
            reverse('budget-ajax-view-subcategory-transactions'))
    add_url_to_context(context, 'create_recurring_transaction',
            reverse('budget-ajax-create-recurring-transaction'))
    add_url_to_context(context, 'get_recurring_transaction',
            reverse('budget-ajax-get-recurring-transaction'))
    add_url_to_context(context, 'save_recurring_transaction',
            reverse('budget-ajax-save-recurring-transaction'))
    add_url_to_context(context, 'apply_recurring_transaction_to_date',
            reverse('budget-ajax-apply-recurring-transaction'))


# vim: et sw=4 sts=4
