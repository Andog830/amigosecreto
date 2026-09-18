from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Participante(models.Model):
    NOMBRES = [
        ('belen', 'Ana Belen'),
        ('sergio', 'Sergio'),
        ('nicolas', 'Nicolás'),
        ('cristhian', 'Christian'),
        ('karen', 'Karen'),
        ('fabian', 'Fabián'),
        ('ricaurte', 'Ricaurte'),
        ('valentina', 'Valsita'),
    ]

    nombre = models.CharField(max_length=30, choices=NOMBRES, unique=True)
    clave = models.CharField(max_length=128)
    registro_generado = models.BooleanField(default=False)

    def establecer_clave(self, clave):
        self.clave = make_password(clave)

    def verificar_clave(self, clave):
        return check_password(clave, self.clave)

    def __str__(self):
        return self.get_nombre_display()