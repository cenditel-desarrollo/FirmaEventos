
from django import forms

from .models import *


class EventoForm(forms.ModelForm):
    """!
    Clase que permite crear el formulario para  el create or update del evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-11-2017
    @version 1.0.0
    """
    archivo = forms.FileField(widget=forms.ClearableFileInput(
                              attrs={'multiple': False}))

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
             'placeholder': 'Fecha'})
        self.fields['archivo'].required=True
        self.fields['archivo'].widget.attrs.update(
            {'class': 'file-path',
             'placeholder': 'Subir Archivo'})

class FirmaEventoForm(forms.Form):
    """!
    Clase que permite crear el formulario para la firma de un documento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    
    pasaporte = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su pasaporte'}))