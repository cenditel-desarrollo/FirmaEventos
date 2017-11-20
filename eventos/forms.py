
from django import forms
from django.forms.fields import (
    CharField, BooleanField
)

from .models import *


class EventoForm(forms.ModelForm):
    """!
    Clase que permite crear el formulario para  el create or update del evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-11-2017
    @version 1.0.0
    """
    #archivo = forms.FileField(widget=forms.ClearableFileInput(
                              #attrs={'multiple': False}))
    archivo = CharField()
    class Meta:
        """!
            Clase que construye los meta datos del formulario
        """
        model = Evento
        exclude = ['activo', 'serial']

    def __init__(self, *args, **kwargs):
        """!
            Funcion que construye los valores iniciales del formulario evento
        """
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['nombre_evento'].widget.attrs.update(
            {'class': 'form-control',
             'placeholder': 'Nombre del evento'})
        self.fields['fecha'].widget.attrs.update(
            {'class': 'datepicker',
             'placeholder': 'Fecha',
             'readonly':
             'readonly'})
        self.fields['archivo'].required=True
        self.fields['archivo'].widget.attrs.update(
            {
            'class': 'file-path validate',
            'placeholder': 'Subur un archivo'})
