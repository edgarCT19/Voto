from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class Usuario(AbstractUser):
    ADMINISTRADOR = 'admin'
    FUNCIONARIO = 'funcionario'
    VOTANTE = 'votante'

    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (FUNCIONARIO, 'Funcionario'),
        (VOTANTE, 'Votante'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default=VOTANTE)
    actas_capturadas = models.PositiveIntegerField(default=0)  # Campo para guardar el número total de actas capturadas por el usuario
    # Otros campos
    
    # Agrega o cambia el argumento related_name en los siguientes campos
    groups = models.ManyToManyField('auth.Group', related_name='usuarios')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='usuarios')

class PartidoPolitico(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    siglas = models.CharField(max_length=10, blank=True)
    logo = models.ImageField(upload_to='partidos/', blank=True)
    votos_totales = models.PositiveIntegerField(default=0, null=True)  # Campo para sumar los votos del partido


class Candidato(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    apellido = models.CharField(max_length=100, null=True)
    partido_politico = models.ForeignKey(PartidoPolitico, on_delete=models.CASCADE, null=True)
    foto_principal = models.ImageField(upload_to='candidatos/', blank=True, null=True)
    foto_secundaria = models.ImageField(upload_to='candidatos/', blank=True, null=True)
    # Agrega más campos de imagen según sea necesario
    
    votos_totales = models.PositiveIntegerField(default=0, null=True)  # Campo para sumar los votos del candidato
    edad = models.PositiveIntegerField(null=True)  # Edad del presidente

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def foto_principal_url(self):
        try:
            url = self.foto_principal.url
        except:
            url = ''
        return url
    
    @property
    def foto_secundaria_url(self):
        try:
            url = self.foto_secundaria.url
        except:
            url = ''
        return url


class Casilla(models.Model):
    nombre = models.CharField(max_length=100, null=True)
    seccion = models.CharField(max_length=50, null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=100, null=True)
    municipio = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=50, null=True)  # Tipo de casilla
    votos_totales = models.PositiveIntegerField(default=0, null=True)  # Campo para sumar los votos de la casilla


class Acta(models.Model):
    fecha = models.DateField(null=True)
    casilla = models.ForeignKey(Casilla, on_delete=models.CASCADE, null=True)
    pdf = models.FileField(upload_to='actas/', null=True)
    votos_partidos = models.JSONField(null=True, blank=True)  # Campo para votos individuales de partidos
    votos_candidatos_independientes = models.PositiveIntegerField(null=True, default=0)
    votos_no_registrados = models.PositiveIntegerField(null=True, default=0)
    votos_nulos = models.PositiveIntegerField(null=True, default=0)


class Voto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)