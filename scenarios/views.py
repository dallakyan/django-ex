from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from matt_django.simple_forms import add_url_to_data
from matt_django.simple_forms import default_model_form
from matt_django.simple_forms import simple_form

from budget.models import Category
from scenarios.models import *
from scenarios.settings import template_base

from collections import namedtuple

@login_required
def main(request):
    data = base_data()
    data['scenarios'] = Scenario.objects.all()
    data['career_paths'] = CareerPath.objects.all()
    data['companies'] = Company.objects.all()
    data['jobs'] = Job.objects.all()
    data['incomes'] = Income.objects.all()
    data['locations'] = Location.objects.all()
    return render(request, template_base + 'main.html', data)


def base_data():
    data = {}
    data['urls'] = []
    return data


def add_location_to_data(data, location):
    data['location'] = location
    data['location_expenses'] = location.expenses()
    add_url_to_data(data,
                    'edit_expenses',
                    reverse('scenarios-ajax-edit-expense'))


def add_income_projections_to_data(data, location, income):
    monthly_expenses = 0
    average_monthly = 0
    if 'location_expenses' not in data:
        data['location_expenses'] = location.expenses()
    expenses = data['location_expenses']
    for expense in expenses:
        monthly_expenses += expense.amount
        average_monthly += expense.average
    TaxCategory = namedtuple('TaxCategory', ['category', 'amount', 'rate'])
    yearly_expenses = monthly_expenses * 12
    yearly_income = income.amount
    yearly_taxes = []
    fed_income_tax = .01 * yearly_income * income.federal_income_tax_rate
    yearly_taxes.append(TaxCategory('Federal Income Tax',
                                    fed_income_tax,
                                    fed_income_tax / yearly_income * 100))
    payroll_tax = .01 * yearly_income * income.payroll_tax_rate
    yearly_taxes.append(TaxCategory('Payroll taxes',
                                    payroll_tax,
                                    payroll_tax / yearly_income * 100))
    city_tax = .01 * yearly_income * location.city_tax_rate
    yearly_taxes.append(TaxCategory('City Income Tax',
                                    city_tax,
                                    city_tax / yearly_income * 100))
    state_income_tax = .01 * yearly_income * location.state_tax_rate
    yearly_taxes.append(TaxCategory('State Income Tax',
                                    state_income_tax,
                                    state_income_tax / yearly_income * 100))
    property_tax = .01 * location.home_price * location.property_tax_rate
    yearly_taxes.append(TaxCategory('Property Tax',
                                    property_tax,
                                    property_tax / yearly_income * 100))
    total_tax = sum(x.amount for x in yearly_taxes)
    yearly_tithing = .12 * yearly_income
    yearly_net_income = (yearly_income
                         - yearly_expenses
                         - total_tax
                         - yearly_tithing)
    data['yearly_expenses'] = yearly_expenses
    data['yearly_income'] = yearly_income
    data['yearly_taxes'] = yearly_taxes
    data['total_tax'] = total_tax
    data['tax_rate'] = total_tax / yearly_income * 100
    data['yearly_tithing'] = yearly_tithing
    data['monthly_expenses'] = monthly_expenses
    data['average_monthly'] = average_monthly
    data['yearly_net_income'] = yearly_net_income
    print data


@login_required
def view_scenario(request, scenario_id):
    data = base_data()
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    data['scenario'] = scenario
    data['income'] = scenario.income
    add_location_to_data(data, scenario.location)
    add_income_projections_to_data(data,
                                   scenario.location,
                                   scenario.income)
    return render(request, template_base + 'scenario.html', data)


@login_required
def view_location(request, location_id):
    data = base_data()
    location = get_object_or_404(Location, pk=location_id)
    add_location_to_data(data, location)
    return render(request, template_base + 'location.html', data)


@login_required
def edit_category_expenses(request):
    category_name = request.POST['category_name']
    location_id = request.POST['location_id']
    amount = request.POST['value'].replace(',', '')
    category = get_object_or_404(Category, name=category_name)
    location = get_object_or_404(Location, pk=location_id)
    location.set_expected_expense(category, int(amount))
    return HttpResponse(amount)


def default_add(request, cls):
    return simple_form(request,
                       default_model_form(cls),
                       reverse('scenarios-main'),
                       'Add %s' % cls.__name__,
                       'Add %s' % cls.__name__,
                       data=base_data())


def default_edit(request, cls, instance_id):
    f = get_object_or_404(cls, pk=instance_id)
    return simple_form(request,
                       default_model_form(cls),
                       reverse('scenarios-main'),
                       'Edit %s' % cls.__name__,
                       'Edit %s' % cls.__name__,
                       data=base_data(),
                       instance=f)


@login_required
def add_career_path(request):
    return default_add(request, CareerPath)


@login_required
def edit_career_path(request, career_path_id):
    return default_edit(request, CareerPath, career_path_id)


@login_required
def add_company(request):
    return default_add(request, Company)


@login_required
def edit_company(request, company_id):
    return default_edit(request, Company, company_id)


@login_required
def add_income(request):
    return default_add(request, Income)


@login_required
def edit_income(request, income_id):
    return default_edit(request, Income, income_id)


@login_required
def add_job(request):
    return default_add(request, Job)


@login_required
def edit_job(request, job_id):
    return default_edit(request, Job, job_id)


@login_required
def add_location(request):
    return default_add(request, Location)


@login_required
def edit_location(request, location_id):
    return default_edit(request, Location, location_id)


@login_required
def add_scenario(request):
    return default_add(request, Scenario)


@login_required
def edit_scenario(request, scenario_id):
    return default_edit(request, Scenario, scenario_id)
