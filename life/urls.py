from django.conf.urls import include, url
from django.contrib.auth.views import login

from life.views import main

urlpatterns = [
    # Main views
    url(r'^$', main),
    url(r'^budget/', include('budget.urls')),
    url(r'^health/', include('health.urls')),
    url(r'^food/', include('food.urls')),
    url(r'^scenarios/', include('scenarios.urls')),

    # Autocomplete stuff
    #url(r'^autocomplete/', include('autocomplete_light.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    # Login stuff
    url(r'^accounts/login/$',
        login,
        {'template_name': 'login.html'}),
]

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
