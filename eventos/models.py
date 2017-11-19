from django.db import models


class Evento(models.Model):
    """!
    Clase que contiene los eventos realizados

    @author Ing. Leonel P. Hernandez M. (lhernandez at cenditel.gob.ve)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
    @date 19-11-2017
    @version 1.0.0
    """
    nombre_evento = models.CharField(max_length=128, unique=True)
    fechao = models.DateField(null=False)
    serial = models.IntegerField(unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        """!
            Clase que construye los meta datos del modelo
        """
        ordering = ('nombre_evento',)
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        db_table = 'eventos_evento'

    def __str__(self):
        """!
        Fucncion que muestra el evento

        @return Devuelve el identificador del evento
        """
        return self.nombre_evento
