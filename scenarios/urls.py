from django.conf.urls import url

from scenarios import views

career_path_id = '(?P<career_path_id>[^/]+)'
company_id = '(?P<company_id>[^/]+)'
income_id = '(?P<income_id>[^/]+)'
job_id = '(?P<job_id>[^/]+)'
location_id = '(?P<location_id>[^/]+)'
scenario_id = '(?P<scenario_id>[^/]+)'

urlpatterns = [
    # Main views
    url(r'^$',
        views.main, name='scenarios-main'),
    url(r'^scenario-'+scenario_id+'$',
        views.view_scenario, name='scenarios-view-scenario'),
    url(r'^location-'+location_id+'$',
        views.view_location, name='scenarios-view-location'),
    # Basic add / edit views for most of the objects
    url(r'^add-scenario$',
        views.add_scenario, name='scenarios-add-scenario'),
    url(r'^edit-scenario/'+scenario_id+'$',
        views.edit_scenario, name='scenarios-edit-scenario'),
    url(r'^add-company$',
        views.add_company, name='scenarios-add-company'),
    url(r'^edit-company/'+company_id+'$',
        views.edit_company, name='scenarios-edit-company'),
    url(r'^add-job$',
        views.add_job, name='scenarios-add-job'),
    url(r'^edit-job/'+job_id+'$',
        views.edit_job, name='scenarios-edit-job'),
    url(r'^add-location$',
        views.add_location, name='scenarios-add-location'),
    url(r'^edit-location/'+location_id+'$',
        views.edit_location, name='scenarios-edit-location'),
    url(r'^add-income$',
        views.add_income, name='scenarios-add-income'),
    url(r'^edit-income/'+income_id+'$',
        views.edit_income, name='scenarios-edit-income'),
    url(r'^add-career-path$',
        views.add_career_path, name='scenarios-add-career-path'),
    url(r'^edit-career-path/'+career_path_id+'$',
        views.edit_career_path, name='scenarios-edit-career-path'),
    # AJAX stuff
    url(r'^ajax-edit-expense/$',
        views.edit_category_expenses, name='scenarios-ajax-edit-expense'),
]

# vim: et sw=4 sts=4
