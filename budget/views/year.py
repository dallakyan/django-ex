from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response

from budget.models import Category
from budget.models import MonthlyBalances
from budget.models import Subcategory
from budget.models import Year
from budget.settings import template_base
from budget.views.general import add_url_to_context
from budget.views.general import base_context

from datetime import date

@login_required
def main(request, year):
    context = base_context(request)
    y = get_object_or_404(Year, year=year)
    context['year'] = y
    context['months'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
            'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Total']
    num_months = len(context['months']) - 1
    context['month_ids'] = []
    # Get total income/expense and net income while we're already going over
    # the months.  TODO(matt): I now have four of these super-categories.
    # Maybe I could handle this better?
    context['total_income'] = [0,] * (num_months + 1)
    context['total_mandatory'] = [0,] * (num_months + 1)
    context['total_investments'] = [0,] * (num_months + 1)
    context['total_expense'] = [0,] * (num_months + 1)
    context['net_income'] = [0,] * (num_months + 1)
    today = date.today()
    for i, month in enumerate(y.month_set.all()):
        context['month_ids'].append(month.id)
        if _is_prior_month(month, today):
            income = month.monthlybalances.total_income
            mandatory = month.monthlybalances.total_mandatory
            investments = month.monthlybalances.total_investments
            expense = month.monthlybalances.total_expense
        elif _is_current_month(month, today):
            # TODO: Handle this month a little differently...?
            income = month.monthlybalances.budgeted_income
            mandatory = month.monthlybalances.budgeted_mandatory
            investments = month.monthlybalances.budgeted_investments
            expense = month.monthlybalances.budgeted_expense
        else:
            try:
                balances = month.monthlybalances
            except MonthlyBalances.DoesNotExist:
                balances = MonthlyBalances(month=month)
                balances.save()
            income = balances.budgeted_income
            mandatory = balances.budgeted_mandatory
            investments = balances.budgeted_investments
            expense = balances.budgeted_expense
        context['total_income'][i] = income
        context['total_income'][-1] += income
        context['total_mandatory'][i] = mandatory
        context['total_mandatory'][-1] += mandatory
        context['total_investments'][i] = investments
        context['total_investments'][-1] += investments
        context['total_expense'][i] = expense
        context['total_expense'][-1] += expense
        context['net_income'][i] = income - expense - mandatory
        context['net_income'][-1] += income - expense - mandatory
    context['month_ids'].append('-1')
    add_url_to_context(context, 'edit_budget',
            reverse('budget-ajax-edit-budget'))
    add_url_to_context(context, 'subcategory_transactions',
            reverse('budget-ajax-view-subcategory-transactions'))
    today = date.today()
    context['current_month'] = today.month
    if y.year == today.year:
        context['relative_year'] = 'current'
    elif y.year < today.year:
        context['relative_year'] = 'past'
    else:
        context['relative_year'] = 'future'
    context['income_categories'] = Category.objects.filter(type='I')
    context['mandatory_categories'] = Category.objects.filter(type='M')
    context['expense_categories'] = Category.objects.filter(type='E')
    context['investment_categories'] = Category.objects.filter(type='V')
    _render_categories(context['income_categories'], num_months, y, -1)
    _render_categories(context['mandatory_categories'], num_months, y, 1)
    _render_categories(context['expense_categories'], num_months, y, 1)
    _render_categories(context['investment_categories'], num_months, y, 1)
    # Calculate category monthly totals (we already have overall totals saved
    # in the database)
    for i in range(num_months+1):
        for category in context['income_categories']:
            for subcat in category.subcategories:
                category.totals[i] += subcat.to_show[i]
        for category in context['mandatory_categories']:
            for subcat in category.subcategories:
                category.totals[i] += subcat.to_show[i]
        for category in context['expense_categories']:
            for subcat in category.subcategories:
                category.totals[i] += subcat.to_show[i]
        for category in context['investment_categories']:
            for subcat in category.subcategories:
                category.totals[i] += subcat.to_show[i]
    prior_balance = _get_prior_balance(y.year)
    context['inactive_subcategories'] = Subcategory.objects.filter(inactive_years=y)
    context['balances'] = [0,] * num_months
    context['balances'][0] = prior_balance + context['net_income'][0]
    for i in range(1, num_months):
        context['balances'][i] = (context['balances'][i-1] +
                context['net_income'][i] - context['total_investments'][i])
    return render_to_response(template_base + 'year.html', context)


def _render_categories(categories, num_months, y, balance_multiplier):
    today = date.today()
    for category in categories:
        category.totals = [0,]*(num_months+1)
        category.rowspan = 0
        category.subcategories = []
        for subcat in category.subcategory_set.all():
            if subcat.inactive_years.filter(year=y.year).exists(): continue
            category.rowspan += 1
            # Balances are negative for income categories, but budgets are
            # positive.  So we only need the balance multiplier for the
            # balance, not for the budget.
            subcat.balances = [balance_multiplier*x for x in
                    subcat.year_balances(y)]
            subcat.budgets = subcat.year_budgets(y)
            if today.year > y.year:
                subcat.to_show = subcat.balances
            elif today.year < y.year:
                subcat.to_show = subcat.budgets
            else:
                subcat.to_show = [0,] * num_months
                for i in range(num_months):
                    if i+1 < today.month:
                        subcat.to_show[i] = subcat.balances[i]
                    else:
                        subcat.to_show[i] = subcat.budgets[i]
            subcat.to_show.append(sum(subcat.to_show))
            category.subcategories.append(subcat)


def _is_prior_month(db_month, today):
    if (db_month.year.year < today.year):
        return True
    if (db_month.year.year > today.year):
        return False
    return db_month.month < today.month


def _is_current_month(db_month, today):
    return db_month.year.year == today.year and db_month.month == today.month


def _get_prior_balance(stopping_year):
    last_known_balance = None
    prior_balance = 0
    for balance in MonthlyBalances.objects.all():
        if balance.month.year.year == stopping_year:
            break
        if last_known_balance and not balance.finalized:
            prior_balance += balance.budgeted_income - balance.budgeted_expense
        elif balance.finalized:
            last_known_balance = balance.final_balance
            prior_balance = balance.final_balance
    return prior_balance

# vim: et sw=4 sts=4
