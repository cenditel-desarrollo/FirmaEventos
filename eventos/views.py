from django.shortcuts import render
from django.views.generic import ListView, FormView
from multi_form_view import MultiModelFormView

from .forms import *
from participantes.forms import (
    FormsetParticipanteEvento
)
from .models import Evento

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


class ListEvent(ListView):
    """!
    Muestra el listado de eventos

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    model = Evento
    template_name = "evento.list.html"
    paginate_by = 5
    
class SignEvent(FormView):
    """!
    Muestra el formulario para buscar y luego firmar documento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    form_class = FirmaEventoForm
    template_name = "evento.firma.html"
    
    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista
    
        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 20-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        kwargs['nombre_evento'] = Evento.objects.get(pk=int(self.kwargs['pk']))
        return super(SignEvent, self).get_context_data(**kwargs)