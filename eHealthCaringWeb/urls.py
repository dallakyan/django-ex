from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from eHealth.models import *

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request):
        #print request
        #searcher=Searcher(age=9)
        #searcher=Searcher.objects.get_or_create(searcher=request)
        print request.email
        #searcher.age=
        searcher= Searcher.objects.create(searcher=request, age=3)
        searcher.age=0
        searcher.email=request.email
        searcher.name= "Add in your info"
        searcher.save()
        #searcher.username
        #sear
        #searcher.save()
        #searcher.gender='Other'
        #searcher.save()

        print request.username
        print "success"

        return '/eHealth/'

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^eHealth/', include('eHealth.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

)
