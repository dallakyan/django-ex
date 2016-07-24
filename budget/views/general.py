from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms

from budget.models import Account
from budget.models import AccountBalance
from budget.models import Category
from budget.models import CategoryBudget
from budget.models import Location
from budget.models import Month
from budget.models import Subcategory
from budget.settings import template_base

from collections import namedtuple
from datetime import date, datetime
import calendar

@login_required
def main(request):
    today = date.today()
    redirect = reverse('budget-month',
            kwargs={'year': today.year, 'month': today.month})
    return HttpResponseRedirect(redirect)


def base_context(request):
    context = RequestContext(request)
    context['template_base'] = template_base
    context['nav_months'] = _get_available_months()
    context['nav_years'] = _get_available_years()
    context['urls'] = []
    return context


def add_url_to_context(context, varname, link):
    Url = namedtuple('Url', ['varname', 'link'])
    context['urls'].append(Url(varname, link))


def _get_available_years():
    # TODO?: combine this with _get_available_months, for fewer DB requests
    # So for now, we're just going to hard code a bunch of years.  Not a great
    # long term solution, but it'll work for now.
    available_years = []
    available_years.append('2012')
    available_years.append('2013')
    available_years.append('2014')
    available_years.append('2015')
    available_years.append('2016')
    available_years.append('2017')
    available_years.append('2018')
    available_years.append('2019')
    available_years.append('2020')
    return available_years


def _get_available_months():
    month_template = namedtuple('MonthTemplate', ['year', 'month', 'text'])
    # All months that have been finalized
    available_months = set()
    for balance in AccountBalance.objects.all():
        m = balance.month
        available_months.add((m.year.year, m.month, str(m)))
    # This month
    today = date.today()
    available_months.add(_month_and_year_from_date_obj(today))
    # Next month
    next_month_year = today.year
    next_month_num = today.month + 1
    if next_month_num > 12:
        next_month_num = 1
        next_month_year += 1
    next_month = date(next_month_year, next_month_num, 1)
    available_months.add(_month_and_year_from_date_obj(next_month))
    # Last month
    last_month_year = today.year
    last_month_num = today.month - 1
    if last_month_num == 0:
        last_month_num = 12
        last_month_year -= 1
    last_month = date(last_month_year, last_month_num, 1)
    available_months.add(_month_and_year_from_date_obj(last_month))
    available_months = list(available_months)
    available_months.sort(reverse=True)
    return [month_template(y, '%02d' % m, text)
            for y, m, text in available_months]


@login_required
@transaction.atomic
def copy_budget_forward(request, year, month):
    m = get_object_or_404(Month, month=month, year__year=year)
    year = int(year)
    next_month = int(month) + 1
    if next_month > 12:
        next_month = 1
        year += 1
    next_m = Month.objects.get(month=next_month, year__year=year)
    for category_budget in m.categorybudget_set.all():
        subcategory = category_budget.subcategory
        subcategory.set_budget(next_m, category_budget.amount)
    redirect = reverse('budget-month',
            kwargs={'year': year, 'month': next_month})
    return HttpResponseRedirect(redirect)


@login_required
def all_locations(request):
    context = base_context(request)
    context['locations'] = Location.objects.all()
    return render_to_response(template_base + 'all_locations.html', context)


def _month_and_year_from_date_obj(date_obj):
    text = calendar.month_name[date_obj.month] + ' ' + str(date_obj.year)
    return (date_obj.year, date_obj.month, text)


def get_current_db_month():
    today = date.today()
    return Month.objects.get(month=today.month, year__year=today.year)


@login_required
def mark_balanced(request):
    f = request.user.finances
    f.last_balanced = datetime.now()
    f.save()
    return HttpResponseRedirect(reverse('budget-main'))


@login_required
def add_account(request):
    return simple_form(request, AccountForm, '/', 'Add Account', 'Add Account')


@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return simple_form(request, AccountForm, '/', 'Edit Account',
            'Edit Account', instance=account)


@login_required
def add_category(request):
    return simple_form(request, CategoryForm, '/', 'Add Category',
            'Add Category')


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return simple_form(request, CategoryForm, '/', 'Edit Category',
            'Edit Category', instance=category)


@login_required
def edit_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    return simple_form(request, LocationForm, '/', 'Edit Location',
            'Edit Location', instance=location)


@login_required
def add_subcategory(request):
    return simple_form(request, SubcategoryForm, '/', 'Add Subcategory',
            'Add Subcategory')


@login_required
def edit_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    return simple_form(request, SubcategoryForm, '/', 'Edit Subcategory',
            'Edit Subcategory', instance=subcategory)


@login_required
def edit_budget(request, year, month, subcategory_id):
    subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
    m = Month.get_month(year, month)
    next_url = reverse('budget-subcategory',
            kwargs={'year': year,
                    'month': month,
                    'subcategory_id': subcategory_id})
    try:
        budget = CategoryBudget.objects.get(subcategory=subcategory, month=m)
    except CategoryBudget.DoesNotExist:
        budget = CategoryBudget(subcategory=subcategory, month=m, amount=0)
        budget.save()
    return simple_form(request, CategoryBudgetForm, next_url, 'Edit Budget',
            'Edit Budget', instance=budget)


@login_required
def simple_form(request, form_class, next_url, label, header, instance=None):
    if request.POST:
        if instance:
            form = form_class(request.POST, instance=instance)
        else:
            form = form_class(request.POST)
        try:
            form.save()
        except ValueError:
            print(form.errors)
            raise
        return HttpResponseRedirect(next_url)
    context = RequestContext(request)
    if instance:
        context['form'] = form_class(instance=instance)
    else:
        context['form'] = form_class()
    context['submit_label'] = label
    context['header'] = header
    return render_to_response('add_form.html', context)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategoryBudgetForm(forms.ModelForm):
    class Meta:
        model = CategoryBudget
        fields = '__all__'
