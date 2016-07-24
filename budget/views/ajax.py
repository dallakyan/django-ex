from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django import forms

from budget.models import Account
from budget.models import ExpenseCategory
from budget.models import Subcategory
from budget.models import Location
from budget.models import Month
from budget.models import RecurringTransaction
from budget.models import Transaction
from budget.settings import template_base
from budget.views.general import base_context

from collections import namedtuple
from dateutil import parser
from decimal import Decimal

@login_required
def month_account(request):
    context = base_context(request)
    m = Month.objects.get(pk=request.GET['month_id'])
    context['month'] = m.month
    context['year'] = m.year.year
    a = Account.objects.get(pk=request.GET['account_id'])
    account_template = namedtuple('AccountTemplate',
            ['id', 'name', 'balance', 'headers', 'transactions'])
    headers = _render_account_headers(a, m)
    transactions = _render_account_transactions(a, m)
    context['account'] = account_template(a.id, a.name,
            a.monthly_balance(m), headers, transactions)
    return render_to_response(template_base + 'month_account.html', context)


@login_required
def edit_category_budget(request):
    subcat_id = request.POST['subcategory_id']
    month_id = request.POST['month_id']
    amount = request.POST['value'].replace(',', '')
    subcategory = get_object_or_404(Subcategory, pk=subcat_id)
    month = get_object_or_404(Month, pk=month_id)
    subcategory.set_budget(month, Decimal(amount))
    return HttpResponse(amount)


@login_required
def add_transaction(request):
    ExpenseFormSet = inlineformset_factory(Transaction, ExpenseCategory,
            fields='__all__', extra=3)
    transaction_id = request.POST.get('transaction_id', None)
    if transaction_id:
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        transaction_form = TransactionForm(request.POST, instance=transaction)
        expense_form = ExpenseFormSet(request.POST, instance=transaction)
    else:
        transaction_form = TransactionForm(request.POST)
        expense_form = ExpenseFormSet(request.POST)
    if not expense_form.is_valid():
        raise ValueError()
    instances = expense_form.save(commit=False)
    if not transaction_form.is_valid():
        raise ValueError()
    transaction = transaction_form.save(commit=False)
    total = Decimal('0.0')
    if transaction_id:
        for form in expense_form.forms:
            amount = form.instance.amount
            if amount:
                total += amount
    else:
        for instance in instances:
            total += instance.amount
    if total != transaction.amount:
        print("Amounts didn't add up:", total, transaction.amount)
        raise ValueError()
    transaction.save()
    for instance in instances:
        instance.transaction = transaction
        instance.save()
    else:
        if transaction_id:
            expense_form.save()
    return HttpResponse('success')


@login_required
def add_transaction_form(request):
    account_id = request.GET['account_id']
    ExpenseFormSet = inlineformset_factory(Transaction, ExpenseCategory,
            fields='__all__', extra=3)
    transaction_id = request.GET.get('transaction_id', None)
    if transaction_id:
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        transaction_form = TransactionForm(instance=transaction)
        expense_form = ExpenseFormSet(instance=transaction)
    else:
        transaction_form = TransactionForm(initial={'account': account_id,
                                                    'pending': True,
                                                    'type': 'D'})
        expense_form = ExpenseFormSet()
    form = transaction_form.as_table() + expense_form.as_table()
    if transaction_id:
        form += '<input type="hidden" name="transaction_id" '
        form += 'value="%s">' % transaction_id
    return HttpResponse(form)


@login_required
def subcategory_transactions(request):
    context = base_context(request)
    m = Month.objects.get(pk=request.GET['month_id'])
    subcat = Subcategory.objects.get(pk=request.GET['subcategory_id'])
    context['expenses'] = []
    expense_template = namedtuple('ExpenseTemplate',
            ['id', 'date', 'amount', 'description', 'location'])
    for e in subcat.expense_set_for_month(m):
        amount = e.amount
        if not e.transaction.is_debit():
            amount = -1 * amount
        context['expenses'].append(expense_template(
                e.transaction.id,
                e.transaction.date,
                amount,
                e.get_description(),
                e.transaction.location,
                ))
    context['subcat_id'] = subcat.id
    context['month'] = m.month
    context['year'] = m.year.year
    context['name'] = subcat.name
    context['balance'] = subcat.monthly_balance(m)
    context['budget'] = subcat.monthly_budget(m)
    context['percent'] = _get_percent_str(context['budget'],
            context['balance'])
    return render_to_response(template_base + 'subcategory_transactions.html', context)


@login_required
def update_pending(request):
    transaction = Transaction.objects.get(pk=request.GET['transaction_id'])
    if (request.GET['is_pending'] == 'true'):
        transaction.pending = True
    else:
        transaction.pending = False
    transaction.save()
    return HttpResponse("success");


@login_required
def edit_transaction_date(request):
    transaction = Transaction.objects.get(pk=request.POST['transaction_id'])
    transaction.date = parser.parse(request.POST['value']).date()
    transaction.save()
    return HttpResponse(request.POST['value']);


@login_required
def edit_transaction_location(request):
    transaction = Transaction.objects.get(pk=request.POST['transaction_id'])
    transaction.location = Location.objects.get(pk=request.POST['location_id'])
    transaction.save()
    return HttpResponse(transaction.location.name);


@login_required
def create_recurring_transaction(request):
    t = RecurringTransaction(name=request.GET['name'])
    t.save()
    return HttpResponse(t.id)


@login_required
def get_recurring_transaction(request):
    t = RecurringTransaction.objects.get(pk=request.GET['id'])
    return HttpResponse(t.transactionsStr)


@login_required
def save_recurring_transaction(request):
    t = RecurringTransaction.objects.get(pk=request.GET['id'])
    t.transactionsStr = pk=request.GET['jsonStr']
    t.save()
    print(vars(t))
    return HttpResponse("Saved!")


@login_required
def apply_recurring_transaction_to_date(request):
    t = RecurringTransaction.objects.get(pk=request.GET['id'])
    import datetime
    date = datetime.datetime.strptime(request.GET['date'], "%m/%d/%Y")
    t.applyTemplatesToDate(date)
    return HttpResponse("Success!")



@login_required
def add_location(request):
    name = request.GET['name']
    response = name
    try:
        Location.objects.get(name=name)
        response += ' already exists'
    except Location.DoesNotExist:
        Location.objects.create(name=name)
        response += ' added'
    return HttpResponse(response)


@login_required
def get_location_selector(request):
    choices = '{'
    for l in Location.objects.all():
        if len(choices) > 1: choices += ','
        choices += '"' + l.name + '-' + str(l.id) + '": "' + l.name + '"'
    choices += '}'
    return HttpResponse(choices)


def _render_account_headers(account, month):
    """Return headers for the table in which transactions will be displayed.

    This should match exactly the fields returned in the render_transactions
    method below (except we do some fudging to get a link out that we can click
    on)."""
    Header = namedtuple('Header', ['text', 'classname'])
    headers = []
    headers.append(Header('Date', 'date'))
    headers.append(Header('Location', 'location'))
    headers.append(Header('Note', 'note'))
    headers.append(Header('Debit', 'dollar-amount'))
    headers.append(Header('Credit', 'dollar-amount'))
    headers.append(Header('Pend', 'pending'))
    headers.append(Header('Bal (A)', 'dollar-amount'))
    headers.append(Header('Bal (P)', 'dollar-amount'))
    return headers


def _render_account_transactions(account, month):
    """Return a set of transactions suitable for rendering"""
    transactions = account.transaction_set_for_month(month)
    rendered = []
    balance = account.get_previous_balance(month, False)
    balance_pending = account.get_previous_balance(month, True)
    TransactionTemplate = namedtuple('TransactionTemplate',
                                     ['id', 'location_id', 'items'])
    Item = namedtuple('Item', ['text', 'classname'])
    t = [Item('', ''), Item('', ''),
            Item('Previous Balance', 'note'), Item('', ''),
            Item('', ''), Item('', ''), Item(balance, 'dollar-amount')]
    if balance == balance_pending:
        t.append(Item('', ''))
    else:
        t.append(Item(balance_pending, 'dollar-amount'))
    rendered.append(TransactionTemplate(-1, -1, t))
    for transaction in transactions:
        t = []
        t.append(Item(transaction.date, 'transaction-date'))
        t.append(Item(transaction.location, 'transaction-location'))
        t.append(Item(transaction.get_description(), 'note'))
        if transaction.pending:
            amount_str = '(%.2f)' % (transaction.amount)
        else:
            amount_str = '%.2f' % (transaction.amount)
        if transaction.is_debit():
            t.append(Item(amount_str, 'dollar-amount'))
            t.append(Item('', ''))
            sign = -1
        else:
            t.append(Item('', ''))
            t.append(Item(amount_str, 'dollar-amount'))
            sign = 1
        balance_pending += sign * transaction.amount
        if transaction.pending:
            t.append(Item('P', 'pending'))
        else:
            balance += sign * transaction.amount
            t.append(Item('', 'pending'))
        t.append(Item(balance, 'dollar-amount'))
        if balance == balance_pending:
            t.append(Item('', ''))
        else:
            t.append(Item(balance_pending, 'dollar-amount'))
        rendered.append(TransactionTemplate(transaction.id,
                                            transaction.location.id,
                                            t))
    return rendered


def _get_percent_str(budget, balance):
    if budget != 0:
        percent = '%.2f' % (Decimal('100.0') * balance / budget)
    else:
        percent = 'N/A'
    return percent


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(active=True)

    class Meta:
        model = Transaction
        fields = '__all__'
