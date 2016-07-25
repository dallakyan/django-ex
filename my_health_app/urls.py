from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^visits/', include('visits.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       # url(r'accounts/logout/', 'visits.views.logout_view'),
                       # url(r'accounts/login/', 'django.contrib.auth.views.login'),
                       url(r'accounts/profile/', 'visits.views.profile_view'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
