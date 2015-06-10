"""securechat URL Configuration

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
from chat_app import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^add_chat/$', views.add_chat, name='add_chat'),
    url(ur'^chat/(?P<chatid>.*)/$', views.chat, name='chat'),
    url(ur'^changeuser/(?P<chatid>.*)/$', views.changeuser, name='changeuser'),
    url(ur'^delete/(?P<chatid>.*)/$', views.delete_chat, name='delete'),
    url(r'^message/(?P<chatid>.*)$', views.message, name='message'),
    url(r'^userlist/(?P<chatid>.*)$', views.user_list, name='user_list'),
    url(r'^admin/', include(admin.site.urls)),
]
