from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from visits import views

urlpatterns = \
patterns('',
         url(r'^$', login_required(views.VisitList.as_view()), name="index"),
         url(r'^providers/$', login_required(views.ProviderList.as_view()), name="providers"),
         url(r'^create/$', login_required(views.VisitCreate.as_view()), name="create"),
         url(r'^(?P<pk>\d+)/edit/$', login_required(views.VisitCreate.as_view()), name="edit"),
         url(r'^(?P<pk>\d+)/$', login_required(views.VisitDetail.as_view()), name="detail"),
         url(r'^email/', views.mail_view),
         )
