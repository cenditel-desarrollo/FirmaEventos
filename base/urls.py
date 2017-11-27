# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', StartView.as_view(), name='inicio'),
]
