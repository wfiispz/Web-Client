"""PZ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from WebClient import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^auth/$', views.auth_view),
    url(r'^logout/$', views.logout),
    url(r'^monitors/$', views.monitors),
    url(r'^create_monitor/$', views.create_monitor),
    url(r'^delete_monitor/(?P<monitor_id>[0-9]+)/$', views.delete_monitor, name='delete'),
    url(r'^invalid/$', views.invalid_login),
    url(r'^register/$', views.register),
    url(r'^register_success/$', views.register_success),
    url(r'^monitor/(?P<monitor_id>[0-9]+)/$', views.hosts, name='host'),
    url(r'^monitor/(?P<monitor_id>[0-9]+)/host/(?P<host_id>[\w-]+)/$', views.measurements, name='measurement'),
    url(r'^monitor/(?P<monitor_id>[0-9]+)/host/(?P<host_id>[\w-]+)/measurements/(?P<measurement_id>[\w-]+)$', views.values, name='value'),
]
