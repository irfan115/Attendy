from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',

                       # grappelli URLS
                       (r'^grappelli/',
                        include('grappelli.urls')),
                       # admin site
                       (r'^admin',
                        include(admin.site.urls)),

                       url(r'^api/',
                           include('api.urls', namespace='api', app_name='api')),

                       url(r'^api-auth/',
                           include('rest_framework.urls', namespace='rest_framework')),



                       )

