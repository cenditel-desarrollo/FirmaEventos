# -*- encoding: utf-8 -*-

import os
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import (
    redirect
)
from django.views import View
from django.views.generic import (
    ListView, FormView
)
from django.views.generic.edit import UpdateView
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
        """!
        Metodo que permite registra y agregar participantes al evento

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 20-11-2017
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna un mensaje de error o exito al success
        """
        nuevo_participante = self.form_participante(request.POST)
        consulta_api = None
        if len(request.FILES)>0:
            file =  request.FILES['file']
            handle_uploaded_file(request.FILES['file'], file)
            ruta = '%s/%s' % (settings.TMP, file)
            file = open(ruta, 'rb')
            files = {'file': file}
            try:
                r = requests.post('https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/cargar', verify=False, headers={'Authorization': 'Basic YWRtaW46YWRtaW4='}, files=files)
                consulta_api = r.json()['fileId']
                # elimina el archivo si fue creado en la carpeta tmp
                file.close()
                os.unlink(ruta)
            except Exception as e:
                print (e)
                file.close()
                os.unlink(ruta)
                messages.error(self.request, "Error al conectar al servidor y subir\
                                              el archivo a la api Murachi")
                return redirect(self.success_url)
        try:

            if self.form_class(request.POST).is_valid() and nuevo_participante.is_valid():
                nuevo_evento = self.form_class(request.POST, request.FILES).save(commit=False)
                nuevo_evento.serial = consulta_api

                for form in nuevo_participante:
                    instance = form.save(commit=False)
                    if instance.nombres == '' or instance.apellidos == '' or instance.pasaporte == '':
                        messages.error(self.request, "Ninguno de los campos del\
                                                      participante puede estar\
                                                      vacio excepto el correo")
                        return redirect(self.success_url)
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
                messages.success(self.request, "El usuario %s, ha creado con exito,\
                                            un nuevo evento %s" %
                                 (str(self.request.user),
                                  str(nuevo_evento)))
            else:
                messages.error(self.request, "Existe un error en el\
                                              Formualario %s %s" %
                               (self.form_class(request.POST).errors,
                                self.form_participante(request.POST).errors))
        except Exception as e:
            print (e)
            messages.error(self.request, "Esta intentando realizar una\
                                          acción incorrecta")

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
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 20-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
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


@method_decorator(csrf_exempt, name='dispatch')
class EventoProcesado(View):
    """!
    Clase que permite consultar si el evento se encuentra disponible para firmar

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 27-11-2017
    @version 1.0.0
    """
    model = Evento

    def get(self, request, event_id):
        """!
        Metodo que permite verificar si el documento esta procesado

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 27-11-2017
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna un Json con la respuesta
        """
        mensaje = ''
        procesando = False
        if event_id is not None:
            try:
                evento_pro = self.model.objects.get(pk=event_id)
            except:
                print(e)
                procesando = True
                mensaje += 'No se encuentra un evento con ese serial'
        else:
            evento_pro = None
            procesando = True
            mensaje += 'No puedes enviar un evento vacio'

        if evento_pro.procesando:
            procesando = True
            mensaje += 'No puedes firmar el documento, en este momento\
                        se encuentra ocupado por otro Usuario'
        else:
            procesando = False
            mensaje += 'Puedes Firmar el Documento'
        data = {'validate': procesando, 'mensaje': mensaje}
        return JsonResponse(data, safe=False)

    def post(self, request, event_id):
        """!
        Metodo que permite cambiar el valor procesado al  evento

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 27-11-2017
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna un Json con la respuesta
        """
        if event_id is not None:
            try:
                evento = self.model.objects.get(pk=event_id)
                evento.procesando = not evento.procesando
                evento.save()
                validado = True
            except:
                print(e)
                validado = False

        return JsonResponse(validado, safe=False)


class UpdateFileEvent(LoginRequiredMixin, FormView):
    """!
    Clase que permite actualizar subir un archivo a un evento que no se haya cargado

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 27-11-2017
    @version 1.0.0
    """
    model = Evento
    form_class = UpdateFileEventoForm
    template_name = 'evento.update.html'
    success_url = reverse_lazy('events:list_events')

    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista

        @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 27-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        evento = int(self.kwargs['event_id'])
        context = super(UpdateFileEvent, self).get_context_data(**kwargs)
        try:
            evento = self.model.objects.select_related().get(pk=evento)
        except Exception as e:
            print(e)
            evento = None
        firma = ParticipanteEvento.objects.filter(fk_evento=evento, firma=True).count()
        if firma >= 1:
            valida = True
        else:
            valida = False

        context['object'] = evento
        context['valida'] = valida
        return context

    def form_valid(self, form):
        """!
        Metodo que permite validar el formulario y agregar archivo al evento

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 27-11-2017
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna un mensaje de error o exito al success
        """
        file =  self.request.FILES['file']
        posx = form.cleaned_data['pos_x']
        posy = form.cleaned_data['pos_y']
        pag = form.cleaned_data['pag']
        consulta_api = None
        try:
            event = Evento.objects.get(pk=int(self.kwargs['event_id']))
        except Exception as e:
            print(e)
            messages.error(self.request, "Error, no se encuentra registrado\
                                          esté evento")
            return redirect(self.success_url)

        handle_uploaded_file(self.request.FILES['file'], file)
        ruta = '%s/%s' % (settings.TMP, file)
        file = open(ruta, 'rb')
        files = {'file': file}
        try:
            r = requests.post('https://murachi.cenditel.gob.ve/Murachi/0.1/archivos/cargar', verify=False, headers={'Authorization': 'Basic YWRtaW46YWRtaW4='}, files=files)
            consulta_api = r.json()['fileId']
            # elimina el archivo si fue creado en la carpeta tmp
            file.close()
            os.unlink(ruta)
        except Exception as e:
            print (e)
            file.close()
            os.unlink(ruta)
            messages.error(self.request, "Error al conectar al servidor y subir\
                                          el archivo a la api Murachi")
            return redirect(self.success_url)

        if event is not None and consulta_api is not None:
            event.serial = consulta_api
            event.pos_x = posx
            event.pos_y = posy
            event.pag = pag
            event.save()
            messages.success(self.request, "El usuario %s, ha actualizado con exito,\
                                            el evento %s" %
                                 (str(self.request.user),
                                  str(event)))
        else:
            messages.error(self.request, "Error al actualizar, debes llenar\
                                          todos los campos, incluyendo la\
                                          configuración de la firma")
        return redirect(self.success_url)


class UpdateEventView(LoginRequiredMixin, UpdateView):
    """!
    Clase que permite actualizar los datos de un evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 28-11-2017
    @version 1.0.0
    """
    model = Evento
    form_class = UpdateEventoForm
    template_name = 'evento.update.participantes.html'
    success_url = reverse_lazy('events:list_events')
    form_participante = FormsetParticipanteEvento

    def get_context_data(self, **kwargs):
        """!
        Metodo que permite cargar de nuevo valores en los datos de contexto de la vista

        @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 28-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param kwargs <b>{object}</b> Objeto que contiene los datos de contexto
        @return Retorna los datos de contexto
        """
        context = super(UpdateEventView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            evento = int(self.kwargs['pk'])
            participante_evento = Participante.objects.filter(participanteevento__fk_evento=evento)
            context['form2'] = self.form_participante(queryset=participante_evento)
        return context

    def post(self, request, *args, **kwargs):
        """!
        Metodo que permite actualizar y agregar mas participantes al evento

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 29-11-2017
        @param request <b>{object}</b> Objeto que contiene la petición
        @return Retorna un mensaje de error o exito al success
        """
        evento = int(self.kwargs['pk'])
        update_participante = self.form_participante(request.POST)
        try:
            if self.form_class(request.POST).is_valid() and update_participante.is_valid():
                evento = self.model.objects.get(pk=evento)
                update_evento = self.form_class(request.POST, instance=evento).save(commit=False)
                for form in update_participante:
                    instance = form.save(commit=False)
                    if instance.nombres == '' or instance.apellidos == '' or instance.pasaporte == '':
                        messages.error(self.request, "Ninguno de los campos del\
                                                      participante puede estar\
                                                      vacio excepto el correo")
                        return redirect(self.success_url)

                update_evento.save()
                # Control para guardar y asignar participantes al evento
                lista_participantes = list(ParticipanteEvento.objects.filter(fk_evento=int(self.kwargs['pk']), firma=False).values('fk_participante__pasaporte'))

                lista_comprobar = []
                for valor in lista_participantes:
                    lista_comprobar += valor.values()
                for form in update_participante:
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        instance = form.save(commit=False)

                        parametros = {
                                        'nombres': instance.nombres,
                                        'apellidos': instance.apellidos,
                                        'correo': instance.correo
                                     }
                        if instance.pasaporte in lista_comprobar:
                            lista_comprobar.remove(instance.pasaporte)
                        update_participante, create = Participante.objects.update_or_create(pasaporte=instance.pasaporte, defaults=parametros)
                        parametro_update = {'fk_participante': update_participante}
                        update_evento_participante, create_part_event = ParticipanteEvento.objects.update_or_create(fk_evento=update_evento, fk_participante__pasaporte=instance.pasaporte, defaults=parametro_update)
                        update_evento_participante.save()
                messages.success(request, "El usuario %s, actualizó el evento %s" % (str(self.request.user), str(update_evento)))
                for valor in lista_comprobar:
                    e = ParticipanteEvento.objects.get(fk_evento=update_evento, fk_participante__pasaporte=valor)
                    e.delete()

            else:
                messages.error(self.request, "Existe un error en el\
                                              Formualario %s %s" %
                               (self.form_class(request.POST).errors,
                                self.form_participante(request.POST).errors))
        except Exception as e:
            print(e)
            messages.error(self.request, "Esta intentando realizar una\
                                          acción incorrecta")
        return redirect(self.success_url)
