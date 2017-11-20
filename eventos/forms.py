
from django import forms
from django.forms.fields import (
    CharField, BooleanField
)

from .models import *


class EventoForm(forms.ModelForm):
    """!
    Clase que permite crear el formulario para  el create or update del evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
<<<<<<< HEAD
            {
            'class': 'file-path validate',
            'placeholder': 'Subur un archivo'})
=======
            {'class': 'file-path',
             'placeholder': 'Subir Archivo'})

class FirmaEventoForm(forms.Form):
    """!
    Clase que permite crear el formulario para la firma de un documento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    
    pasaporte = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su pasaporte'}))
>>>>>>> def10d28a56c05436aa09889ff50481aaec4bc4a
