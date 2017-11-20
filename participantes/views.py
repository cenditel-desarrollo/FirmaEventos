from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import ParticipanteEvento

class ParticipanteEventoSearch(TemplateView):
    """!
    Muestra si un participante esta registrado en un evento

    @author Rodrigo Boet  (rboet at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 20-11-2017
    @version 1.0.0
    """
    template_name = "inicio.html"
        
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
                        'pasaporte':pasaporte,'correo':p.fk_participante.correo}}
        return JsonResponse(data,safe=False)
