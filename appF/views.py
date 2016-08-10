from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from .forms import RegistroUserForm
from .models import UserProfile, enfermedad, medicamento, medicamento_enfermedad, farmacia_medicamento
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required



def registro_usuario_view(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')
            user_model = User.objects.create_user(username=username, password=password)
            user_model.email = email
            user_model.save()
            nombre = cleaned_data.get('nombre')
            apellido = cleaned_data.get('apellido')
            direccion = cleaned_data.get('direccion')
            tipo = cleaned_data.get('tipo')
            edad = cleaned_data.get('edad')
            peso = cleaned_data.get('peso')
            telefono = cleaned_data.get('telefono')
            user_profile = UserProfile()
            user_profile.user = user_model
            user_profile.nombre = nombre
            user_profile.apellido = apellido
            user_profile.direccion = direccion
            user_profile.tipo = tipo
            user_profile.edad = edad
            user_profile.peso = peso
            user_profile.telefono = telefono
            user_profile.save()
            return redirect('../')

    else:
        form = RegistroUserForm()
    context = {
        'form': form
    }
    return render(request, 'registro.html', context)

def inicio(request):
    mensaje = ''
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    if acceso.userprofile.tipo == 'cliente':
                        return redirect('/cliente')
                    else:
                        return render_to_response('farmaceutico.html')
                else:
                    return render_to_response('noactivo.html')
            else:
                return render_to_response('nousuario.html')
    else:
        formulario = AuthenticationForm()
        return render(request, 'inicio.html', {'formulario':formulario})

@login_required(login_url='/')
def salir(request):
    logout(request)
    return redirect('../')

@login_required(login_url='/')
def listarProductos(request):
    usuario = request.user
    enfermedades = enfermedad.objects.all()
    context = {
        'enfermedades':enfermedades,
        "usuario":usuario
        }
    return render(request, 'cliente.html', context)

@login_required(login_url='/')
def listarMedicamento(request):
    usuario = request.user
    ide=request.GET['id']
    medicamento = medicamento_enfermedad.objects.filter(idenfermedad = ide)
    enfermedades = enfermedad.objects.get(id = ide)
    context = {
        'medicamento':medicamento,
        "usuario":usuario,
        "enfermedades": enfermedades
        }
    return render(request, 'listarMedicamentos.html', context)

@login_required(login_url='/')
def listarFarmacias(request):
    usuario = request.user
    idm=request.GET['id']
    farmacia = farmacia_medicamento.objects.filter(idmedicamento = idm)
    medicamentos = medicamento.objects.get(id = idm)
    context = {
        'farmacia':farmacia,
        "usuario":usuario,
        "medicamentos": medicamentos
        }
    return render(request, 'listarFarmacias.html', context)
