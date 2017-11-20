from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from multi_form_view import MultiModelFormView
from django.views.generic import FormView

from .forms import *
from participantes.forms import (
    FormsetParticipanteEvento
)

class RegisterEvent(FormView):
    """!
    Muestra el formulario de registro de usuarios

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """

    template_name = "register.event.html"
    form_class = EventoForm
    form_participante = FormsetParticipanteEvento
    success_url = reverse_lazy('base:inicio')

    def get_context_data(self, **kwargs):
        context = super(RegisterEvent, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.form_participante
        return context

    def post(self, request, *args, **kwargs):
        nuevo_evento = self.form_class(request.POST).save(commit=False)
        nuevo_participante = self.form_participante(request.POST)
        consulta_api = 1
        if self.form_class(request.POST).is_valid() and nuevo_participante.is_valid():
            nuevo_evento.serial = consulta_api
            nuevo_evento.save()
            nuevo_participante.save()
            messages.success(self.request, "El usaurio %s, ha creado con exito,\
                                        un nuevo envento %s" %
                         (str(self.request.user),
                          str(nuevo_evento)))
        else:
            messages.error(self.request, "Existe un error en el Formualario %s" %
                         (str(self.form_class.errors, self.form_participante.errors)))
        return redirect(self.success_url)
