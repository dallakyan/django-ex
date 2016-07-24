from django.conf.urls import url

from budget.views import year as year_view
from budget.views import month as month_view
from budget.views import general as general_view
from budget.views import ajax as ajax_view

account_id = '(?P<account_id>\d+)'
category_id = '(?P<category_id>\d+)'
location_id = '(?P<location_id>\d+)'
month = '(?P<month>\d\d?)'
month_id = '(?P<month_id>\d\d?)'
subcategory_id = '(?P<subcategory_id>\d+)'
transaction_id = '(?P<transaction_id>\d+)'
year = '(?P<year>\d\d\d\d)'


urlpatterns = [
    # Main views
    url(r'^$',
        general_view.main, name='budget-main'),
    url(r'^'+year+'/$',
        year_view.main, name='budget-year'),
    url(r'^'+year+'/'+month+'/$',
        month_view.main, name='budget-month'),
    url(r'^'+year+'/'+month+'/location/'+location_id+'/$',
        month_view.location, name='budget-location-by-month'),
    url(r'^'+year+'/location/'+location_id+'/$',
        month_view.location, name='budget-location-by-year'),
    url(r'^location/'+location_id+'/$',
        month_view.location, name='budget-location-all-time'),
    url(r'^locations$',
        general_view.all_locations, name='budget-all-locations'),

    # Form views
    url(r'^add_account$',
        general_view.add_account, name='budget-add-account'),
    url(r'^edit_account/'+account_id+'$',
        general_view.edit_account, name='budget-edit-account'),
    url(r'^add_category$',
        general_view.add_category, name='budget-add-category'),
    url(r'^edit_category/'+category_id+'$',
        general_view.edit_category, name='budget-edit-category'),
    url(r'^edit_location/'+location_id+'$',
        general_view.edit_location, name='budget-edit-location'),
    url(r'^add_subcategory$',
        general_view.add_subcategory, name='budget-add-subcategory'),
    url(r'^edit_subcategory/'+subcategory_id+'$',
        general_view.edit_subcategory, name='budget-edit-subcategory'),
    url(r'^'+year+'/'+month+'/category/'+subcategory_id+'/edit_budget$',
        general_view.edit_budget, name='budget-edit-budget'),

    # AJAX requests
    url(r'^ajax/edit_category_budget$',
        ajax_view.edit_category_budget, name='budget-ajax-edit-budget'),
    url(r'^mark-balanced$',
        general_view.mark_balanced, name='budget-mark-balanced'),
    url(r'^ajax/month_account$',
        ajax_view.month_account, name='budget-ajax-month-account'),
    url(r'^ajax/update_pending$',
        ajax_view.update_pending, name='budget-ajax-update-pending'),
    url(r'^ajax/edit_transaction_date$',
        ajax_view.edit_transaction_date, name='budget-ajax-edit-transaction-date'),
    url(r'^ajax/edit_transaction_location$',
        ajax_view.edit_transaction_location,
        name='budget-ajax-edit-transaction-location'),
    url(r'^ajax/get_location_selector$',
        ajax_view.get_location_selector, name='budget-ajax-get-location-selector'),
    url(r'^ajax/add_location$',
        ajax_view.add_location, name='budget-ajax-add-location'),
    url(r'^ajax/add_transaction$',
        ajax_view.add_transaction, name='budget-ajax-add-transaction'),
    url(r'^ajax/add_transaction_form$',
        ajax_view.add_transaction_form, name='budget-ajax-add-transaction-form'),
    url(r'^ajax/subcategory_transactions$',
        ajax_view.subcategory_transactions, name='budget-ajax-view-subcategory-transactions'),
    url(r'^ajax/create_recurring_transaction$',
        ajax_view.create_recurring_transaction, name='budget-ajax-create-recurring-transaction'),
    url(r'^ajax/get_recurring_transaction$',
        ajax_view.get_recurring_transaction, name='budget-ajax-get-recurring-transaction'),
    url(r'^ajax/save_recurring_transaction$',
        ajax_view.save_recurring_transaction, name='budget-ajax-save-recurring-transaction'),
    url(r'^ajax/apply_recurring_transaction_to_date$',
        ajax_view.apply_recurring_transaction_to_date, name='budget-ajax-apply-recurring-transaction'),

    # Redirect requests
    url(r'^'+year+'/'+month+'/finalize$',
        month_view.finalize_month, name='budget-finalize-month'),
    url(r'^'+year+'/'+month+'/copy-budget-forward$',
        general_view.copy_budget_forward, name='budget-copy-budget-forward'),
]

# vim: et sw=4 sts=4
