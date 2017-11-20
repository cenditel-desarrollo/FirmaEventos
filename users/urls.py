# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.views import (
    password_reset, password_reset_done,
    )

from .forms import PasswordResetForm
from .views import *


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogOutView.as_view(), name="logout"),

     # Reset password all users
    url(r'^password/reset/$', password_reset,
        {'post_reset_redirect': '/password/done/',
         'template_name': 'users_forgot.html',
         'password_reset_form': PasswordResetForm},
        name="forgot"),
    url(r'^password/done/$', password_reset_done,
        {'template_name': 'users_pass_reset_done.html'},
        name='reset_done'),

]