from django import forms
from django.forms import (
       inlineformset_factory,
   )

from eventos.model import (
    Evento
    )
from .models import *

class ParticiapanteForm(forms.ModelForm):
    """!
    Clase que crea el formulario para  el create or update del participante

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-11-2017
    @version 1.0.0
    """

    class Meta:
        """!
            Clase que construye los meta datos del formulario
        """
        model = Participante
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
            """!
                Funcion que construye los valores iniciales del formulario participante
            """
            super(ParticiapanteForm, self).__init__(*args, **kwargs)
            self.fields['fk_evento'].widget.attrs.update(
                    {'class': 'form-control'})
            self.fields['fk_evento'].label = 'Evento en el que participa'
            self.fields['nombres'].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Nombres'})
            self.fields['apellidos'].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Apellidos'})
            self.fields['identidad'].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Pasaporte'})
            self.fields['correo'].widget.attrs.update(
                    {'class': 'form-control',
                     'placeholder': 'Correo'})


class AddPartEventForm(forms.ModelForm):
    """!
    Clase que crea el formulario para  añadir participante al evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-11-2017
    @version 1.0.0
    """

    class Meta:
        """!
            Clase que construye los meta datos del formulario
        """
        model = ParticipanteEvento
        exclude = ['firma', 'fk_evento']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "El participante ya se\
                encuentra registrado en el evento.",
            }
        }

    def __init__(self, *args, **kwargs):
        """!
            Funcion que construye los valores iniciales del participante evento
        """
        super(AddPartEventForm, self).__init__(*args, **kwargs)
        self.fields['fk_participante'].empty_label = 'Seleccione Participante'
        self.fields['fk_participante'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['fk_participante'].label = 'Participante'


FormsetObj = inlineformset_factory(
                                    Evento, ParticipanteEvento,
                                    form=AddPartEventForm,
                                    fields=('fk_participante',),
                                    fk_name='fk_evento', min_num=1,
                                    extra=0, validate_min=True,
                                    can_delete=True)
