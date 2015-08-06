"""streak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'goals.views.index', name='index'),
    url(r'^goal/(?P<goal_id>[0-9]+)/$', 'goals.views.goal', name='goal'),
    url(r'^login/$', 'goals.views.login_view', name='login'),
    url(r'^logout/$', 'goals.views.logout_view', name='logout'),
    url(r'^goal/$', 'goals.views.new_goal', name='new_goal'),
    url(r'^delete_goal/(?P<goal_id>[0-9]+)/$', 'goals.views.delete_goal', name='delete_goal'),
    url(r'^about/$', 'goals.views.about_view', name='about'),
    url(r'^contact/$', 'goals.views.contact_view', name='contact'),
    url(r'^update_goal/(?P<goal_id>[0-9]+)/$', 'goals.views.update_goal', name='update_goal'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^goal_settings/(?P<goal_id>[0-9]+)/$', 'goals.views.goal_settings', name='goal_settings'),
    url(r'^account/$', 'goals.views.account_page_view', name='account_page'),
]
