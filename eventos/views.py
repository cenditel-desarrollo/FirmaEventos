from django.shortcuts import render
from multi_form_view import MultiModelFormView

from .forms import *
from participantes.forms import (
    FormsetParticipanteEvento
)

class RegisterEvent(MultiModelFormView):
    """!
    Muestra el formulario de registro de usuarios

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    template_name = "register.event.html"
    form_classes = {
      'event': EventoForm,
      'participante': FormsetParticipanteEvento,
    }
    #success_url = reverse_lazy('users:home')
    record_id=None
