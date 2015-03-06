from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$','mysite.views.home'),
     url(r'^cpanel/',include('cpanel.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/root/djcode/mysite/template'})
)
