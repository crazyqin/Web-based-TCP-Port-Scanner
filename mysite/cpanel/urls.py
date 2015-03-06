from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/root/djcode/mysite/template/css'}),
     url(r'^js/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/root/djcode/mysite/template/js'}),
     url(r'^img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/root/djcode/mysite/template/img'}),
     url(r'^login$','cpanel.views.userlogin'),
     url(r'^logout$','cpanel.views.userlogout'),
     url(r'^dashboard$','cpanel.views.dashboard'),
     url(r'^addDevice$','cpanel.devices.addDevice'),
     url(r'^deviceList$','cpanel.devices.deviceList'),
     url(r'^device-(?P<deviceid>\d*)$','cpanel.devices.deviceDetail'),
     url(r'^delDevice-(?P<deviceid>\d*)$','cpanel.devices.delDevice'),
     url(r'^editDevice-(?P<deviceid>\d*)$','cpanel.devices.editDevice'),
     url(r'^portScan$','cpanel.system.portScan'),
     url(r'^portscanResult$','cpanel.system.portscanResult'),
     url(r'^portscanResult/(?P<path>.*)$','django.views.static.serve',{'document_root':'/root/djcode/mysite/'}),
     #url(r'^portscanresultClear$','cpanel.system.portscanresultClear'),
     #url(r'^portscanresultClear/(?P<deviceip>.*)$','cpanel.system.portscanresultClear')
)
