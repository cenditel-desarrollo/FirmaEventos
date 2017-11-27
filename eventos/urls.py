# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

urlpatterns = [
    # Url Access Super Admin
    # Crear y asignar participantes a eventos
    url(r'^crear-eventos/$', RegisterEvent.as_view(), name='create_events'),
    #Url Access all Users
    url(r'^lista-eventos/$', ListEvent.as_view(), name='list_events'),
    url(r'^firmar-evento/(?P<pk>\d+)$', SignEvent.as_view(),
        name='firma_events'),
    url(r'^detail-evento/(?P<pk>\d+)$', DetailEvent.as_view(),
        name='detail_event'),
    url(r'^comprobar-evento/(?P<event_id>\d+)$', EventoProcesado.as_view(),
        name='comprobar_evento'),
    url(r'^comprobar-evento/$', EventoProcesado.as_view(),
        name='comprobar_evento_nid'),
    url(r'^actualizar-evento/(?P<event_id>\d+)$', UpdateFileEvent.as_view(),
        name='update_evento'),
]
