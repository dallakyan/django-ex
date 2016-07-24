#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'life.settings'
sys.path.append(".")

import django
django.setup()

from budget.models import *
from health.models import *
from food.models import *
from health.views import *
from django.contrib.auth.models import User
from django.db import transaction
import datetime

@transaction.atomic
def fix_monthly_balances():
    today = datetime.date.today()
    for month in Month.objects.all():
        print month
        prior_month = (month.year.year < today.year or
                (month.year.year == today.year and month.month < today.month))
        budgeted_income = 0
        final_income = 0
        for c in Category.objects.filter(type='I'):
            budgeted_income += c.monthly_budget(month)
            if prior_month:
                # Balance is negative for income, but budget is positive
                final_income -= c.monthly_balance(month)
        budgeted_mandatory = 0
        final_mandatory = 0
        for c in Category.objects.filter(type='M'):
            budgeted_mandatory += c.monthly_budget(month)
            if prior_month:
                final_mandatory += c.monthly_balance(month)
        budgeted_expense = 0
        final_expense = 0
        for c in Category.objects.filter(type='E'):
            budgeted_expense += c.monthly_budget(month)
            if prior_month:
                final_expense += c.monthly_balance(month)
        budgeted_investments = 0
        final_investments = 0
        for c in Category.objects.filter(type='V'):
            budgeted_investments += c.monthly_budget(month)
            if prior_month:
                final_investments += c.monthly_balance(month)
        try:
            balances = month.monthlybalances
        except MonthlyBalances.DoesNotExist:
            balances = MonthlyBalances(month=month)
        balances.budgeted_income = budgeted_income
        balances.budgeted_mandatory = budgeted_mandatory
        balances.budgeted_expense = budgeted_expense
        balances.budgeted_investments = budgeted_investments
        balances.total_income = final_income
        balances.total_mandatory = final_mandatory
        balances.total_expense = final_expense
        balances.total_investments = final_investments
        balances.save()


def fix_income_budgets():
    transaction.set_autocommit(False)
    for budget in CategoryBudget.objects.filter(
            subcategory__category__type='I'):
        if budget.amount < 0:
            budget.amount *= -1
        budget.save()
    transaction.commit()
    transaction.set_autocommit(True)


if __name__ == '__main__':
    fix_monthly_balances()
    #fix_income_budgets()

# vim: et sw=4 sts=4
