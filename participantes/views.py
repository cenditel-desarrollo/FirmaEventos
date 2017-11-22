from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import (
    ParticipanteEvento, Participante
)
from eventos.models import (
    Evento
)

class ParticipanteEventoSearch(View):
    """!
    Muestra si un participante esta registrado en un evento

    @author Rodrigo Boet  (rboet at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 20-11-2017
    @version 1.0.0
    """

    def get(self,request,pk,pasaporte):
        """!
        Metodo para antender la vista por GET

        @author Rodrigo Boet (rboet at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 20-11-2017
        @param self <b>{object}</b> Objeto que instancia la clase
        @param request <b>{object}</b> Objeto que contiene la petición
        @param pk <b>{int}</b> Recibe el id del evento
        @param pasaporte <b>{str}</b> Recibe el número de pasaporte
        @return Retorna un Json con la respuesta
        """
        participante = ParticipanteEvento.objects.filter(fk_evento=pk,fk_participante__pasaporte=pasaporte)
        data = {}
        if(participante):
            p = participante.get()
            data = {'firmo':p.firma,'datos':{'nombres':p.fk_participante.nombres,'apellidos':p.fk_participante.apellidos,
                        'pasaporte':pasaporte,'correo':p.fk_participante.correo,'documento':p.fk_evento.serial}}
        return JsonResponse(data,safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class AjaxParticipanteFirmaEvento(View):
    """!
    Ajax para sincronizar la firma del participante

    @author Leonel P. Hernandez M.  (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 21-11-2017
    @version 1.0.0
    """
    model = Evento
    model_participante = ParticipanteEvento

    def post(self, request):
        """!
        Metodo para antender la vista por POST

        @author Leonel P. Hernandez M (lhernandez at cenditel.gob.ve)
        @copyright GNU/GPLv3
        @date 21-11-2017
        @return Retorna un Json con la respuesta
        """
        data = {}
        validate = False
        mensaje = ''
        evento_id = request.POST.get('event_id', None)
        print(evento_id)
        serial = request.POST.get('serial', None)
        print(serial)
        pasaporte = request.POST.get('pasaporte', None)
        print(pasaporte)
        if evento_id is not None and pasaporte is not None:
            if serial is not None:
                try:
                    update_evento = self.model.objects.get(pk=evento_id)
                    update_evento.serial = serial
                    update_evento.save()
                    mensaje += 'Se actualizo el serial del evento \n'
                except Exception as e:
                    print (e)
                    validate = False
                    mensaje += 'No existe el evento que desea actualizar \n'
            try:
                participante = Participante.objects.get(pasaporte=pasaporte)
            except Exception as e:
                print (e)
                validate = False
                mensaje += 'El pasaporte no coincide con los\
                            participantes que se ecuentran registrados \n'
            try:
                update_parti_event = self.model_participante.objects.get(
                                    fk_participante=participante.pk,
                                    fk_evento=evento_id)
                update_parti_event.firma = True
                update_parti_event.save()
                mensaje += 'Se actualizo la firma del participante %s, \
                para el evento %s' % (update_parti_event.fk_participante.nombres,
                                      update_parti_event.fk_evento.nombre_evento)
                validate = True
            except Exception as e:
                print(e)
                validate = False
                mensaje += 'El evento no esta asociado al participante\
                            o no se encuentra registrado\n'

        else:
            mensaje += 'Debes enviar al menos\
                        dos argumentos (evento_id, pasaporte)'
            validate = False
        data = {'validate': validate, 'mensaje': mensaje}

        return JsonResponse(data, safe=False)
