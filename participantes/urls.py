# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^search-participante/(?P<pk>\d+)/(?P<pasaporte>.+)$', ParticipanteEventoSearch.as_view(), name='search_participante'),
    url(r'^search-participante/$', ParticipanteEventoSearch.as_view(), name='search_participante_nid'),
    url(r'^update-participante-evento/$', AjaxParticipanteFirmaEvento.as_view(), name='update_participante_evento'),
    url(r'^participante-restante/(?P<evento>\d+)/$', ParticipantesRestantes.as_view(), name='participante_restante_evento'),
    url(r'^participante-restante/$', ParticipantesRestantes.as_view(), name='participante_restante_evento_nid'),
]
