from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm  # Importa el formulario de inicio de sesión
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Candidato
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Voto
from .models import Acta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Acta, Candidato, User, PartidoPolitico
from django.db.models import Sum 
from .forms import ActaForm, CandidatoForm
from django.shortcuts import render, redirect
from .models import PartidoPolitico
from .forms import PartidoPoliticoForm
# Create your views here.


def login_view(request):  # Cambia el nombre de la función de vista
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirige a la página de inicio después del inicio de sesión exitoso
        else:
            # Mensaje de error de inicio de sesión
            return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas. Inténtelo de nuevo.'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    total_actas = Acta.objects.count()
    total_votos_nulos = Acta.objects.aggregate(total_nulos=Sum('votos_nulos'))['total_nulos'] or 0 # type: ignore
    actas = Acta.objects.all()

    context = {
        'total_actas': total_actas,
        'total_votos_nulos': total_votos_nulos,
        'actas': actas,  # Pasar los datos de Acta al contexto
    }

    if request.user.rol == 'admin':
        return render(request, 'admin/home.html', context)
    elif request.user.rol == 'funcionario':
        return render(request, 'funcionario/home.html', context)
    else:
        return render(request, 'home.html', context)
    
@login_required   
def logout_view(request):
    logout(request)
    return redirect('login') 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Lógica para asignar roles según el formulario de registro
            rol = request.POST.get('rol')  # Suponiendo que tienes un campo 'rol' en tu formulario de registro
            user.rol = rol
            user.save()
            auth_login(request, user)  # Autenticar al usuario después del registro
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def total_actas(request):
    # Obtiene el total de actas capturadas
    total_actas_capturadas = Acta.objects.count()
    return render(request, 'ruta_de_tu_template/total_actas.html', {'total_actas_capturadas': total_actas_capturadas})

@login_required
def user(request):
    candidatos = Candidato.objects.all()
    total_actas = Acta.objects.count()
    total_votos_nulos = Acta.objects.aggregate(total_nulos=Sum('votos_nulos'))['total_nulos'] or 0  # type: ignore
    total_votos_no_registrados = Acta.objects.aggregate(total_no_registrados=Sum('votos_no_registrados'))['total_no_registrados'] or 0  # type: ignore
    total_votos_independientes = Acta.objects.aggregate(total_independientes=Sum('votos_candidatos_independientes'))['total_independientes'] or 0  # type: ignore
    
    # Calcular los votos de los partidos
    actas = Acta.objects.all()
    total_votos_partidos = 0
    for acta in actas:
        if acta.votos_partidos:
            if isinstance(acta.votos_partidos, int):
                total_votos_partidos += acta.votos_partidos
            else:
                # Si votos_partidos no es un entero, podría manejar esto de otra manera
                pass

    total_votos_generales = (
        total_votos_nulos + 
        total_votos_no_registrados + 
        total_votos_independientes + 
        total_votos_partidos
    )

    context = {
        'candidatos': candidatos,
        'total_actas': total_actas,
        'total_votos_nulos': total_votos_nulos,
        'total_votos_no_registrados': total_votos_no_registrados,
        'total_votos_independientes': total_votos_independientes,
        'total_votos_partidos': total_votos_partidos,
        'total_votos_generales': total_votos_generales,
        'actas': actas,
    }

    return render(request, 'home.html', context)

def candidates_data(request):
    candidatos = Candidato.objects.all()
    data = list(candidatos.values('nombre', 'apellido', 'votos_totales'))
    return JsonResponse(data, safe=False)

@login_required
def votacion(request):
    # Verifica si el usuario ya ha votado
    if Voto.objects.filter(usuario_id=request.user.id).exists():
        return render(request, 'user/ya_votaste.html')
    
    candidatos = Candidato.objects.all()
    return render(request, 'user/votacion.html', {'candidatos': candidatos})

@login_required
def registrar_voto(request):
    if request.method == 'POST':
        candidato_id = request.POST.get('candidato_id')
        user_id = request.user.id
        try:
            # Verifica si el usuario ya ha votado por ese candidato
            if Voto.objects.filter(usuario_id=user_id, candidato_id=candidato_id).exists():
                return HttpResponse('Ya no puedes votar, ya has emitido tu voto', status=403)
            
            # Obtén el candidato y registra el voto del usuario
            candidato = Candidato.objects.get(id=candidato_id)
            candidato.votos_totales += 1
            candidato.save()
            
            # Registra el voto del usuario
            Voto.objects.create(usuario_id=user_id, candidato_id=candidato_id)
            
            return HttpResponse('Voto registrado exitosamente.')
        except Candidato.DoesNotExist:
            return HttpResponse('Candidato no encontrado.', status=404)
    else:
        return HttpResponse('Método no permitido.', status=405)
    
def funcionario(request):
    actas = Acta.objects.all()
    return render(request, 'funcionario/home.html', {'actas': actas})

def adminHome(request):
    users = User.objects.all()
    return render(request, 'admin/home.html', {'users': users})

def candidatos(request):
    candidatos = Candidato.objects.all()
    return render(request, 'admin/registerCandidato.html', {'candidatos': candidatos})

def register_form(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('candidatos')  # Redirige a la página de candidatos después de registrar uno nuevo
    else:
        form = CandidatoForm()
    return render(request, 'admin/register_form.html', {'form': form})

def partidos(request):
    partidos = PartidoPolitico.objects.all()  # Suponiendo que tengas un modelo Partido definido
    return render(request, 'admin/partidos.html', {'partidos': partidos})

def register_acta(request):
    if request.method == 'POST':
        form = ActaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('funcionario')  # Redirigir a la página de inicio del funcionario
    else:
        form = ActaForm()
    return render(request, 'funcionario/register_acta.html', {'form': form})

def votos_partidos(request): #Vista del candidato (register_candidato)
    candidatos = Candidato.objects.all()
    return render(request, 'funcionario/votos_partidos.html', {'candidatos': candidatos})

def sumar_votos(request):
    if request.method == 'POST':
        candidato_id = request.POST.get('candidato')
        votos = int(request.POST.get('votos'))

        candidato = Candidato.objects.get(pk=candidato_id)
        candidato.votos_totales += votos
        candidato.save()

        return redirect('funcionario')  # Redirige a la página principal del funcionario después de registrar los votos
    
    candidatos = Candidato.objects.all()
    return render(request, 'funcionario/sumar_voto.html', {'candidatos': candidatos})

def register_form(request): #Vista del candidato (register_candidato)
    return render(request, 'admin/register_form.html')

def register_funcionario(request):
    return render(request, 'admin/register_funcionario.html')

def register_partido(request):
    if request.method == 'POST':
        form = PartidoPoliticoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('partidos')  # Redirige a la página de partidos después de registrar uno nuevo
    else:
        form = PartidoPoliticoForm()
    
    return render(request, 'admin/register_partido.html', {'form': form})

def edit_candidato(request):
    return render(request, 'admin/edit_candidato.html')

def edit_funcionario(request):
    return render(request, 'admin/edit_funcionario.html')

def edit_partido(request, partido_id):
    partido = PartidoPolitico.objects.get(pk=partido_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        siglas = request.POST.get('siglas')
        logo = request.FILES.get('logo')
        
        partido.nombre = nombre
        partido.siglas = siglas
        if logo:
            partido.logo = logo
        partido.save()
        
        return redirect('partidos')  # Redirige a la página de partidos después de editar
    
    return render(request, 'admin/edit_partido.html', {'partido': partido})

def delete_funcionario(request):
    return render(request, 'admin/home.html')

def delete_partido(request, partido_id):
    partido = PartidoPolitico.objects.get(id=partido_id)
    # Aquí puedes agregar lógica para eliminar el partido
    partido.delete()
    return redirect('partidos')

def delete_candidato(request):
    return render(request, 'admin/home.html')

def conteo(request):
    return render(request, 'admin/conteo.html')