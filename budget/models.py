from django.db import models
from django.db import transaction
from datetime import date

import calendar
import json
from decimal import Decimal

class Finances(models.Model):
    # Holds some global state, like when the finances were last balanced.
    # Assuming there's only one user, this is a reasonable enough way to make
    # this unique.  If the number of users changes, though, this might need
    # some work.
    user = models.OneToOneField('auth.User')
    last_balanced = models.DateTimeField()


class Account(models.Model):
    name = models.CharField(max_length=128)

    def transaction_set_for_month(self, month):
        first_date, last_date = get_dates_for_month(month)
        t = self.transaction_set.filter(date__gte=first_date,
                date__lte=last_date)
        return t

    def __unicode__(self):
        return self.name

    def transaction_total(self, transactions, include_pending):
        total = 0
        for t in transactions:
            if t.type == 'C':
                sign = 1
            else:
                sign = -1
            if include_pending or not t.pending:
                total += sign * t.amount
        return total

    def monthly_balance(self, month, include_pending=False, recalculate=False):
        # First try just looking up the balance
        if not recalculate:
            try:
                return self.accountbalance_set.get(month=month).balance
            except AccountBalance.DoesNotExist:
                pass
        balance = self.get_previous_balance(month, include_pending)
        # Now add the current month's transactions
        transactions = self.transaction_set_for_month(month)
        return balance + self.transaction_total(transactions, include_pending)

    def balance(self, include_pending=False):
        # Go through all transactions in order to get the current balance
        transactions = self.transaction_set.all()
        return self.transaction_total(transactions, include_pending)

    def balance_pending(self):
        return self.balance(include_pending=True)

    def get_previous_balance(self, month, include_pending):
        """Returns the account balance on the first day of the month, before
        any transactions.  If the value is saved, we just return the saved
        value; otherwise, we calculate it."""
        # First see if we can just short circuit the calculation because we
        # have a saved value
        try:
            return self.accountbalance_set.get(month=month.previous()).balance
        except AccountBalance.DoesNotExist:
            pass
        # I could look for a previous saved balance, but it's probably not
        # worth it, unless this has, like, thousands or tens of thousands of
        # transactions.
        first_date, _ = get_dates_for_month(month)
        transactions = self.transaction_set.filter(date__lt=first_date)
        return self.transaction_total(transactions, include_pending)

    class Meta:
        ordering = ['name']


class Year(models.Model):
    year = models.IntegerField()

    def previous(self):
        try:
            return Year.objects.get(year=self.year-1)
        except Year.DoesNotExist:
            y = Year(year=self.year-1)
            y.save()
            return y

    def next(self):
        try:
            return Year.objects.get(year=self.year+1)
        except Year.DoesNotExist:
            y = Year(year=self.year+1)
            y.save()
            return y

    def __unicode__(self):
        return str(self.year)

    class Meta:
        ordering = ['year']


class Month(models.Model):
    month = models.IntegerField()
    year = models.ForeignKey('Year')

    @staticmethod
    def get_month(year, month):
        y = Year.objects.get(year=year)
        return Month.objects.get(year=y, month=month)

    def previous(self):
        year = self.year
        month = self.month - 1
        if month == 0:
            year = year.previous()
            month = 12
        try:
            return Month.objects.get(year=year, month=month)
        except Month.DoesNotExist:
            m = Month(year=year, month=month)
            m.save()
            return m

    def next(self):
        year = self.year
        month = self.month + 1
        if month == 13:
            year = year.next()
            month = 1
        try:
            return Month.objects.get(year=year, month=month)
        except Month.DoesNotExist:
            m = Month(year=year, month=month)
            m.save()
            return m

    def __unicode__(self):
        return calendar.month_name[self.month] + ' ' + unicode(self.year)

    class Meta:
        ordering = ['year', 'month']


class MonthlyBalances(models.Model):
    month = models.OneToOneField('Month')
    finalized = models.BooleanField(default=False)
    budgeted_income = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    budgeted_mandatory = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    budgeted_investments = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    budgeted_expense = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    # These three fields are only meaningful if finalized == True.
    total_income = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    total_mandatory = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    total_investments = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    total_expense = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)
    final_balance = models.DecimalField(default=Decimal('0.0'),
            decimal_places=2, max_digits=7)

    def budgeted_net_income(self):
        return self.budgeted_income - self.budgeted_expense

    class Meta:
        ordering = ['month']


class AccountBalance(models.Model):
    account = models.ForeignKey('Account')
    month = models.ForeignKey('Month')
    balance = models.DecimalField(decimal_places=2, max_digits=8)


class Category(models.Model):
    name = models.CharField(max_length=128)
    TYPE_CHOICES = (
            (u'I', u'Income'),
            (u'M', u'Mandatory'),
            (u'E', u'Expense'),
            (u'V', u'Investment')
            )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name

    def monthly_budget(self, month):
        budget = 0
        for subcat in self.subcategory_set.all():
            budget += subcat.monthly_budget(month)
        return budget

    def monthly_balance(self, month):
        balance = 0
        for subcat in self.subcategory_set.all():
            balance += subcat.monthly_balance(month)
        return balance

    def balance(self):
        balance = 0
        for subcat in self.subcategory_set.all():
            balance += subcat.balance()
        return balance

    class Meta:
        ordering = ['name']


class Subcategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey('Category')
    inactive_years = models.ManyToManyField('Year', blank=True)

    def __unicode__(self):
        return self.name

    def expense_set_for_month(self, month):
        first_date, last_date = get_dates_for_month(month)
        return self.expensecategory_set.filter(
                transaction__date__gte=first_date,
                transaction__date__lte=last_date)

    def expense_total(self, expenses, include_pending):
        total = 0
        for expense in expenses:
            if expense.transaction.is_debit():
                sign = 1
            else:
                sign = -1
            if include_pending or not expense.transaction.pending:
                total += sign * expense.amount
        return total

    def set_budget(self, month, amount):
        prev_budget = 0
        try:
            budget = self.categorybudget_set.get(month=month)
            prev_budget = budget.amount
            budget.amount = amount
            budget.save()
        except CategoryBudget.DoesNotExist:
            budget = self.categorybudget_set.create(amount=amount, month=month)
        difference = budget.amount - prev_budget
        try:
            balances = month.monthlybalances
        except MonthlyBalances.DoesNotExist:
            balances = MonthlyBalances(month=month)
            balances.save()
        if self.category.type == 'I':
            balances.budgeted_income += difference
        if self.category.type == 'M':
            balances.budgeted_mandatory += difference
        elif self.category.type == 'E':
            balances.budgeted_expense += difference
        elif self.category.type == 'V':
            balances.budgeted_investments += difference
        balances.save()

    def monthly_budget(self, month):
        try:
            budget = self.categorybudget_set.get(month=month).amount
        except CategoryBudget.DoesNotExist:
            budget = 0
        return budget

    def monthly_balance(self, month, include_pending=True):
        expenses = self.expense_set_for_month(month)
        return self.expense_total(expenses, include_pending)

    @transaction.atomic
    def year_balances(self, year):
        today = date.today()
        current_month = today.month
        current_year = today.year
        balances = []
        for month in year.month_set.all():
            if current_year > year.year or (current_year == year.year
                    and current_month > month.month):
                # The month we're getting a balance for has already happened;
                # there should be a CategoryBalance for it.  If not, we'll
                # create one and save the balance.
                try:
                    cat_balance = self.categorybalance_set.get(month=month)
                except CategoryBalance.DoesNotExist:
                    amount = self.monthly_balance(month)
                    cat_balance = CategoryBalance(subcategory=self,
                            month=month, amount=amount)
                    cat_balance.save()
                balances.append(cat_balance.amount)
            elif current_year == year.year and current_month == month.month:
                # This month - just add our current balance, whatever it is
                balances.append(self.monthly_balance(month))
            else:
                # This is in the future; we'll just calculate whatever's
                # pending, like if we've scheduled recurring payments already.
                # I may want to change this to just be zero, but we'll see.
                balances.append(self.monthly_balance(month))
        return balances

    @transaction.atomic
    def year_budgets(self, year):
        budgets = []
        for month in year.month_set.all():
            # Just grab the value from the database, and create an empty value,
            # if it doesn't exist.
            try:
                cat_budget = self.categorybudget_set.get(month=month)
            except CategoryBudget.DoesNotExist:
                cat_budget = CategoryBudget(subcategory=self,
                        month=month, amount=Decimal('0.0'))
                cat_budget.save()
            budgets.append(cat_budget.amount)
        return budgets

    def balance(self, include_pending=True):
        expenses = self.expensecategory_set.all()
        return self.expense_total(expenses, include_pending)

    def balance_pending(self):
        return self.balance(include_pending=True)

    class Meta:
        ordering = ['name']


class CategoryBudget(models.Model):
    subcategory = models.ForeignKey('Subcategory')
    month = models.ForeignKey('Month')
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    note = models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        name = self.subcategory.name
        return name + ', ' + str(self.month) + ": " + str(self.amount)


class CategoryBalance(models.Model):
    subcategory = models.ForeignKey('Subcategory')
    month = models.ForeignKey('Month')
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    note = models.CharField(max_length=512)

    def __unicode__(self):
        name = self.subcategory.name
        return name + ', ' + str(self.month) + ": " + str(self.amount)


class Location(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def transaction_set_for_month(self, month):
        first_date, last_date = get_dates_for_month(month)
        return self.transaction_set.filter(
                date__gte=first_date,
                date__lte=last_date)

    def transaction_set_for_year(self, year):
        first_date, last_date = get_dates_for_year(year)
        return self.transaction_set.filter(
                date__gte=first_date,
                date__lte=last_date)

    def total_spent(self):
        total = 0
        for transaction in self.transaction_set.all():
            if transaction.is_debit():
                total += transaction.amount
            else:
                total -= transaction.amount
        return total

    def total_spent_in_month(self, month):
        total = 0
        transactions = self.transaction_set_for_month(month)
        for transaction in transactions:
            if transaction.is_debit():
                total += transaction.amount
            else:
                total -= transaction.amount
        return total

    # TODO(matt): This is a general method that doesn't need to be here.
    def transaction_total(self, transaction_set):
        total = 0
        for transaction in transaction_set:
            if transaction.is_debit():
                total += transaction.amount
            else:
                total -= transaction.amount
        return total

    class Meta:
        ordering = ['name']


class RecurringTransaction(models.Model):
    name = models.CharField(max_length=128)
    transactionsStr = models.TextField(default='[]')

    def decodeTransactions(self):
        if self.transactionsStr:
            return json.loads(self.transactionsStr)
        else:
            return []

    def addTransaction(self, account, location, amount, type, subcategory, note=""):
        transactions = self.decodeTransactions()
        transaction = {}
        transaction['account'] = account
        transaction['location'] = location
        transaction['amount'] = amount
        transaction['subcategory'] = subcategory
        transaction['type'] = type
        transaction['note'] = note
        transactions.append(transaction)
        self.transactionsStr = json.dumps(transactions)
        self.save()

    def applyTemplatesToDate(self, date):
        for transaction in self.decodeTransactions():
            t = Transaction(account=Account.objects.get(name=transaction['account']),
                            date=date,
                            amount=transaction['amount'],
                            notes=transaction['note'],
                            location=Location.objects.get(name=transaction['location']),
                            type=transaction['type'][0],
                            pending=True
                            )
            t.save()
            expense = ExpenseCategory(transaction=t,
                                      subcategory=Subcategory.objects.get(name=transaction['subcategory']),
                                      amount=transaction['amount']
                                      )
            expense.save()

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    account = models.ForeignKey('Account')
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    notes = models.CharField(max_length=512, blank=True)
    location = models.ForeignKey('Location')
    TYPE_CHOICES = ((u'C', u'Credit'), (u'D', u'Debit'))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    pending = models.BooleanField()

    def get_description(self):
        note = self.notes
        expenses = self.expensecategory_set.all()
        if len(expenses) == 1:
            if not note:
                note = expenses[0].description
        categories = [(e.subcategory, e.amount) for e in expenses]
        if len(expenses) == 1:
            cat_str = categories[0][0]
        else:
            cat_str = ', '.join('%s: %.2f' % (c[0], c[1]) for c in categories)
        return '%s (%s)' % (note, cat_str)

    def is_debit(self):
        return self.type == u'D'

    def expenses(self):
        return self.expensecategory_set.all()

    class Meta:
        ordering = ['date']


class ExpenseCategory(models.Model):
    transaction = models.ForeignKey('Transaction')
    subcategory = models.ForeignKey('Subcategory')
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    description = models.CharField(max_length=512, blank=True)

    def get_description(self):
        if self.description:
            return self.description
        return self.transaction.notes
    class Meta:
        ordering = ['transaction__date']



def get_dates_for_month(month):
    year_num = month.year.year
    month_num = month.month
    first_day = 1
    first_date = date(year_num, month_num, first_day)
    last_day = calendar.monthrange(year_num, month_num)[1]
    last_date = date(year_num, month_num, last_day)
    return first_date, last_date

def get_dates_for_year(year):
    year_num = year.year
    first_day = 1
    first_date = date(year_num, 1, first_day)
    last_day = calendar.monthrange(year_num, 12)[1]
    last_date = date(year_num, 12, last_day)
    return first_date, last_date

