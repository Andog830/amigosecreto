from django.contrib import admin

from .models import Participante


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'registro_generado')
    list_filter = ('registro_generado',)