
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views
app_name = 'accounts'

urlpatterns = [

    url(r'login/$', views.user_login, name="user_login"),
    url(r'logout/$', views.user_logout, name="user_logout"),
    url(r'register/$', views.register, name="register"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password-reset/$',
        auth_views.PasswordResetView.as_view(template_name="posts/password_reset_form.html"),
        name='password_reset'),
    url(r'^password-reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="posts/password_reset_done.html"),
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="posts/password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name="posts/password_reset_complete.html"),
        name='password_reset_complete'),
]
