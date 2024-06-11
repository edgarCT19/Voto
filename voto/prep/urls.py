from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.user, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name="register"),
    path('registrar_voto/', views.registrar_voto, name='registrar_voto'),
    path('votos_partidos/', views.sumar_votos, name='sumar_votos'),
    path('sumar_votos/', views.votos_partidos, name='votos_partidos'),
    path('total_actas/', views.total_actas, name='total_actas'),
    path('funcionario/', views.funcionario, name="funcionario"),
    path('candidates/data/', views.candidates_data, name='candidates_data'),
    path('adminHome/', views.adminHome, name="adminHome"),
    path('votacion/', views.votacion, name="votacion"),
    path('registrar_voto/', views.registrar_voto, name='registrar_voto'),
    path('candidatos/', views.candidatos, name="candidatos"),
    path('partidos/', views.partidos, name="partidos"),
    path('register_acta/', views.register_acta, name="register_acta"),
    path('register_form/', views.register_form, name="register_form"),
    path('register_partido/', views.register_partido, name="register_partido"),
    path('register_funcionario/', views.register_funcionario, name="register_funcionario"),
    path('edit_candidato/', views.edit_candidato, name="edit_candidato"),
    path('edit_partido/', views.edit_partido, name="edit_partido"),
    path('edit_funcionario/', views.edit_funcionario, name="edit_funcionario"),
    path('edit_partido/<int:partido_id>/', views.edit_partido, name='edit_partido'),
    path('delete_partido/<int:partido_id>/', views.delete_partido, name='delete_partido'),
    path('conteo/', views.conteo, name="conteo"),
]