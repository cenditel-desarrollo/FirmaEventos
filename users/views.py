# -*- encoding: utf-8 -*-
"""!
Vista que controla los procesos de los usuarios

@author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
@copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
@date 09-01-2017
@version 1.0.0
"""
from django.core import serializers
from django import forms
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate, logout, login
)

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.models import (
    Group, Permission, User
)
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.validators import validate_email
from django.core.urlresolvers import (
    reverse_lazy, reverse
)

from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from multi_form_view import MultiModelFormView
from .forms import FormularioLogin
from base.views import LoginRequeridoPerAuth
from base.messages import MENSAJES_LOGIN, MENSAJES_START

class LoginView(FormView):
    """!
    Muestra el formulario de ingreso a la aplicación 

    @author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    """
    form_class = FormularioLogin
    template_name = 'users_login.html'
    success_url = reverse_lazy('base:inicio')

    def form_valid(self, form):
        """
        Valida el formulario de logeo
        @return: Dirige a la pantalla inicial de la plataforma
        """
        usuario = form.cleaned_data['usuario']
        contrasena = form.cleaned_data['contrasena']
        try:
            validate_email(usuario)
            try:
                usuario = User.objects.get(email=usuario).username
            except:
                messages.error(self.request, 'No existe este correo: %s \
                                              asociado a una cuenta' % (usuario))
        except Exception as e:
            print (e)


        usuario = authenticate(username=usuario, password=contrasena)
        print(usuario, contrasena)
        if usuario is not None:
            login(self.request, usuario)

            if self.request.POST.get('remember_me') is not None:
                # Session expira a los dos meses si no se deslogea
                self.request.session.set_expiry(1209600)
            messages.info(self.request, MENSAJES_START['INICIO_SESION'] % (usuario.first_name, usuario.username))
        else:
            self.success_url = reverse_lazy('users:login')
            user = User.objects.filter(username=form.cleaned_data['usuario'])
            if user:
                user = user.get()
                if not user.is_active:
                    messages.error(self.request, MENSAJES_LOGIN['CUENTA_INACTIVA'])
                else:
                    messages.warning(self.request, MENSAJES_LOGIN['LOGIN_USUARIO_NO_VALIDO'])

        return super(LoginView, self).form_valid(form)


class LogOutView(RedirectView):
    """!
    Salir de la apliacion

    @author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    """
    permanent = False
    query_string = True

    def get_redirect_url(self):
        """!
        Dirige a la pantalla del login
        @return: A la url del login
        """
        logout(self.request)
        return reverse_lazy('users:login')
