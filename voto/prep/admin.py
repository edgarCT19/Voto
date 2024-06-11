from django.contrib import admin
from .models import Usuario, PartidoPolitico, Candidato, Casilla, Acta, Voto

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol')
    list_filter = ('rol',)

@admin.register(PartidoPolitico)
class PartidoPoliticoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')

@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'partido_politico')

@admin.register(Casilla)
class CasillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'seccion', 'ciudad', 'municipio', 'tipo')

@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'casilla')

@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'candidato')
