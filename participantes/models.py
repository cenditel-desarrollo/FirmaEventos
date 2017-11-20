from django.db import models

from eventos.models import (
    Evento
    )

class Participante(models.Model):
    """!
    Clase que contiene los datos de los participantes

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 19-11-2017
    @version 1.0.0
    """
    nombres = models.CharField(max_length=128)
    apellidos = models.CharField(max_length=128)
    pasaporte = models.CharField(max_length=20,unique=True)
    correo = models.EmailField(max_length=78, null=True)

    class Meta:
        ordering = ('pasaporte',)
        verbose_name = 'Participante'
        verbose_name_plural = 'Participantes'
        db_table = 'participantes_participante'

    def __str__(self):
        """!
        Fucncion que muestra lla informacion del participante

        @return Devuelve el identificador de la opcion
        """
        return str(self.pasaporte)+" | "+str(self.nombres)+" "+str(self.apellidos)


class ParticipanteEvento(models.Model):
    """!
    Clase que contiene los datos que relaciona un usuario al evento

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='https://www.gnu.org/licenses/gpl-3.0.en.html'>GNU Public License versión 3 (GPLv3)</a>
    @date 19-11-2017
    @version 1.0.0
    """

    fk_participante = models.ForeignKey(Participante)
    fk_evento = models.ForeignKey(Evento)
    firma = models.BooleanField(default=False)

    class Meta:
        unique_together = (('fk_evento',  'fk_participante'),)

    def __str__(self):
        """!
        Fucncion que muestra la identidad del participante

        @return Devuelve el identificador de la opcion
        """
        return str(self.fk_participante)
