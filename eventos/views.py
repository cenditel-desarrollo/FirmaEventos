# -*- encoding: utf-8 -*-

import os
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import (
    redirect
)
from django.views.generic import (
    ListView, FormView
)
from django.views.generic.detail import DetailView

from multi_form_view import MultiModelFormView

from .forms import *
from participantes.forms import (
    FormsetParticipanteEvento
)
from .models import Evento
from participantes.models import (
    Participante, ParticipanteEvento
)


def handle_uploaded_file(file, name):
    with open('%s/%s' % (settings.TMP, name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

class RegisterEvent(LoginRequiredMixin, FormView):
    """!
    Muestra el formulario de registro de usuarios

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
            context['form2'] = self.form_participante(queryset=Participante.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        file =  request.FILES['file']
        handle_uploaded_file(request.FILES['file'], file)
        ruta = '%s/%s' % (settings.TMP, file)
        file = open(ruta, 'rb')
        files = {'file': file}
        try:
            r = requests.post('https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/cargar', verify=False, headers={'Authorization': 'Basic YWRtaW46YWRtaW4='}, files=files)
            nuevo_participante = self.form_participante(request.POST)
            consulta_api = r.json()['fileId']
            # elimina el archivo si fue creado en la carpeta tmp
            file.close()
            os.unlink(ruta)
        except Exception as e:
            print (e)
            file.close()
            os.unlink(ruta)
            messages.error(self.request, "Error al concetar al servidor y subir\
                                          el archivo a la api Murachi")
            return redirect(self.success_url)
        try:
            if self.form_class(request.POST).is_valid() and nuevo_participante.is_valid():
                nuevo_evento = self.form_class(request.POST, request.FILES).save(commit=False)
                nuevo_evento.serial = consulta_api
                nuevo_evento.save()
                # Control para guardar y asignar participantes al evento
                for form in nuevo_participante:
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        instance = form.save(commit=False)
                        parametros = {
                                        'nombres': instance.nombres,
                                        'apellidos': instance.apellidos,
                                        'correo': instance.correo
                                        }
                        nuevo_participante, create = Participante.objects.update_or_create(pasaporte=instance.pasaporte, defaults=parametros)
                        asigna_evento = ParticipanteEvento(
                                        fk_participante=nuevo_participante,
                                        fk_evento=nuevo_evento)
                        asigna_evento.save()
                messages.success(self.request, "El usaurio %s, ha creado con exito,\
                                            un nuevo envento %s" %
                                 (str(self.request.user),
                                  str(nuevo_evento)))
            else:
                messages.error(self.request, "Existe un error en el\
                                              Formualario %s %s" %
                               (self.form_class(request.POST).errors,
                                self.form_participante(request.POST).errors))
        except Exception as e:
            print (e)
            messages.error(self.request, "Esta intentado realizar una\
                                          accion incorrecta")

        return redirect(self.success_url)


class ListEvent(ListView):
    """!
    Muestra el listado de eventos

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
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


class DetailEvent(DetailView):
    """!
    Muestra el detalle del evento

    @author Rodrigo Boet (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    model = Evento
    template_name = "evento.detail.html"

    def get_context_data(self, **kwargs):
        evento = int(self.kwargs['pk'])
        context = super(DetailEvent, self).get_context_data(**kwargs)
        try:
            participante_evento = ParticipanteEvento.objects.select_related().filter(fk_evento=evento)
            falta_porfirma = participante_evento.filter(firma=False).count()
        except Exception as e:
            print(e)
            participante_evento = None
            falta_porfirma = None
        context['participantes'] = participante_evento
        context['num_firma'] = falta_porfirma
        return context
