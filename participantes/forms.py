from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import (
       inlineformset_factory, modelform_factory, modelformset_factory, formset_factory
   )

from eventos.models import (
    Evento
    )
from .models import *


class ParticiapanteForm(forms.ModelForm):
    """!
    Clase que crea el formulario para  el create or update del participante

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 19-11-2017
    @version 1.0.0
    """

    class Meta:
        """!
            Clase que construye los meta datos del formulario
        """
        model = Participante
        fields=['nombres', 'apellidos', 'pasaporte', 'correo']

    def __init__(self, *args, **kwargs):
            """!
                Funcion que construye los valores iniciales del formulario participante
            """
            super(ParticiapanteForm, self).__init__(*args, **kwargs)
            self.fields['nombres'].widget.attrs.update(
                    {'placeholder': 'Nombres'})
            self.fields['apellidos'].widget.attrs.update(
                    {'placeholder': 'Apellidos'})
            self.fields['pasaporte'].widget.attrs.update(
                    {'placeholder': 'Pasaporte'})
            self.fields['correo'].widget.attrs.update(
                    {'placeholder': 'Correo'})


class AddPartEventForm(forms.ModelForm):
    """!
    Clase que crea el formulario para  añadir participante al evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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


FormsetEventPartici = inlineformset_factory(
                                    Evento, ParticipanteEvento,
                                    form=AddPartEventForm,
                                    fields=('fk_participante',),
                                    fk_name='fk_evento', min_num=1,
                                    extra=0, validate_min=True,
                                    can_delete=True)

FormsetParticipanteEvento = modelform_factory(
                                    Participante,
                                    form=ParticiapanteForm,
                                    fields=('nombres', 'apellidos',
                                            'pasaporte', 'correo'))

FormsetParticipanteEvento = modelformset_factory(
                            Participante,
                            form=FormsetParticipanteEvento,
                            fields=('nombres', 'apellidos',
                                    'pasaporte', 'correo'),
                            extra=1, validate_min=True,
                            can_delete=True)
