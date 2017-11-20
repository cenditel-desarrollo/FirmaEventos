# -*- coding: utf-8 -*-
"""!
Modulo Forms  que construye los formularios para los templates  de la plataforma

@author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
@copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
@date 09-06-2017
@version 1.0.0
"""
from captcha.fields import CaptchaField
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, PasswordResetForm,
    SetPasswordForm
    )
from django.forms.fields import (
    CharField, BooleanField
)
from django.forms.widgets import (
    PasswordInput, CheckboxInput
)

class FormularioLogin(forms.Form):
    """!
    Clase que permite crear el formulario de ingreso a la aplicación

    @author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    """
    contrasena = CharField()
    usuario = CharField()
    remember_me = BooleanField()
    captcha = CaptchaField()

    class Meta:
        fields = ('usuario', 'contrasena', 'remember_me' 'captcha')

    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['contrasena'].widget = PasswordInput()
        self.fields['contrasena'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Contraseña'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-control',
        'placeholder': 'Nombre de Usuario'})
        self.fields['remember_me'].label = "Recordar"
        self.fields['remember_me'].widget = CheckboxInput()
        self.fields['remember_me'].required = False
        self.fields['captcha'].required=True


class PasswordResetForm(PasswordResetForm):
    """!
    Clase que permite sobrescribir el formulario para resetear la contraseña

    @author Ing. Leonel P. Hernandez M. (leonelphm at gmail.com)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 09-01-2017
    @version 1.0.0
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Dirección de Correo'})

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get("email")

        if email:
            msg = "Error este email: %s, no se encuentra asociado a una cuenta\
                  " % (email)
            try:
                User.objects.get(email=email)
            except:
                self.add_error('email', msg)


class SetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Ingresa la nueva contraseña'})

        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'Repite la nueva contraseña'})


