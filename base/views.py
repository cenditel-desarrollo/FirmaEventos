# -*- coding: utf-8 -*-
"""!
Vista que construye los controladores para las utilidades de la plataforma

@author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
@copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
@date 09-06-2017
@version 1.0.0
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from dal import autocomplete
from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import (
    PermissionRequiredMixin, LoginRequiredMixin
)
from django.shortcuts import (
    redirect
)

from .models import *
from .messages import MENSAJES_LOGIN


class LoginRequeridoPerAuth(LoginRequiredMixin, GroupRequiredMixin):
    """!
    Clase que construye el controlador para el login requerido, se sobreescribe el metodo dispatch

    @author Ing. Leonel Paolo Hernandez Macchiarulo  (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-06-2017
    @version 1.0.0
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Envia una alerta al usuario que intenta acceder sin permisos para esta clase
        @return: Direcciona al login en caso de no poseer permisos, en caso contrario accede a la clase
        """
        if not request.user.is_authenticated:
            messages.warning(self.request, MENSAJES_LOGIN['LOGIN_REQUERIDO'])
            return self.handle_no_permission()
        valid_group = False
        grupos = request.user.groups.all()
        grupo = []
        if len(grupos) > 1:
            for g in grupos:
                grupo += str(g),
                if (str(g) in self.get_group_required()):
                    valid_group = True
        else:
            try:
                grupo = str(request.user.groups.get())
            except:
                return redirect('users:403error')
            if (grupo in self.get_group_required()):
                valid_group = True
        if not (valid_group):
            return redirect('users:403error')
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StartView(TemplateView):
    """!
    Muestra el inicio de la plataforma

    @author Ing. Leonel Paolo Hernandez Macchiarulo  (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    @return: El template inicial de la plataforma
    """
    template_name = "index.html"
