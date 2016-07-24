from django.db import models

from collections import namedtuple
from collections import defaultdict
from datetime import date

from budget.models import CategoryBalance

class Scenario(models.Model):
    job = models.ForeignKey('Job')
    income = models.ForeignKey('Income')
    location = models.ForeignKey('Location')
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return (unicode(self.job) +
                ' in ' + unicode(self.location) +
                ' making ' + unicode(self.income))


class Income(models.Model):
    amount = models.IntegerField()
    federal_income_tax_rate = models.FloatField()
    payroll_tax_rate = models.FloatField()

    def __unicode__(self):
        return (unicode(self.amount) +
                ' (income tax: %.2f)' % self.federal_income_tax_rate)

    class Meta:
        ordering = ['amount']


class Job(models.Model):
    company = models.ForeignKey('Company')
    title = models.CharField(max_length=256)
    career_path = models.ForeignKey('CareerPath')
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return '%s at %s (%s)' % (self.title,
                                  unicode(self.company),
                                  unicode(self.career_path))

    class Meta:
        ordering = ['company', 'career_path']


class Location(models.Model):
    name = models.CharField(max_length=256)
    city_tax_rate = models.FloatField()
    state_tax_rate = models.FloatField()
    home_price = models.IntegerField()
    property_tax_rate = models.FloatField()
    notes = models.TextField(blank=True)

    categories_to_ignore = (
            'Bookkeeping',
            'Income',
            'Tithing and Offerings',
            )

    def expenses(self):
        today = date.today()
        first_month = date(2012, 12, 1)
        months = (12*(today.year - first_month.year)
                  + today.month - first_month.month)
        Expense = namedtuple('Expense', ['category', 'amount', 'average'])
        expenses = self.locationcategoryexpenses_set.all()
        expenses_dict = defaultdict(LocationCategoryExpenses)
        for expense in expenses:
            expenses_dict[expense.category] = expense
        expenses = []
        category_totals = defaultdict(float)
        for balance in CategoryBalance.objects.select_related().all():
            category = balance.subcategory.category
            if category.name in self.categories_to_ignore: continue
            category_totals[category] += float(balance.amount)
        for category in category_totals:
            average = category_totals[category] / months
            amount = expenses_dict[category].amount
            if not amount:
                amount = 0
            expenses.append(Expense(category=category.name,
                                    amount=amount,
                                    average=average))
        return expenses

    def set_expected_expense(self, category, amount):
        try:
            expense = self.locationcategoryexpenses_set.get(category=category)
        except LocationCategoryExpenses.DoesNotExist:
            expense = LocationCategoryExpenses(location=self,
                                               category=category)
        expense.amount = amount
        expense.save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Company(models.Model):
    name = models.CharField(max_length=256)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CareerPath(models.Model):
    name = models.CharField(max_length=256)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class LocationCategoryExpenses(models.Model):
    location = models.ForeignKey('Location')
    category = models.ForeignKey('budget.Category')
    amount = models.IntegerField()
