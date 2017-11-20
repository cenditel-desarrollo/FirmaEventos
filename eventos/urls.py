# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

urlpatterns = [
    # Urls Access Super Admin
    # Crear y asignar participantes a eventos
    url(r'^crear-eventos/$', RegisterEvent.as_view(), name='create_events'),
    url(r'^lista-eventos/$', ListEvent.as_view(), name='list_events'),
]
