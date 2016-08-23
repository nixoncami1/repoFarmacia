from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from .forms import RegistroUserForm, RegistroFarmacia, RegistroMedicamento, RegistroMedicamentoFarmacia
from .models import UserProfile, enfermedad, farmacia, medicamento, medicamento_enfermedad, farmacia_medicamento, farmacia_persona
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
import json as simplejson
import json


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
            user_profile.contra = password
            user_profile.save()
            return redirect('../')

    else:
        form = RegistroUserForm()
    context = {
        'form': form
    }
    return render(request, 'registro.html', context)

def regFarm(request):
    if request.method == 'POST':
        form = RegistroFarmacia(request.POST)
        usuario = request.user
        up = UserProfile.objects.get(user = usuario)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombre = cleaned_data.get('nombre')
            direccion = cleaned_data.get('direccion')
            telefono = cleaned_data.get('telefono')
            latitud = cleaned_data.get('latitud')
            longitud = cleaned_data.get('longitud')
            Farmacia = farmacia()
            Farmacia.nombre = nombre
            Farmacia.direccion = direccion
            Farmacia.telefono = telefono
            Farmacia.latitud = latitud
            Farmacia.longitud = longitud
            Farmacia.idpersona = up
            Farmacia.save()
            return redirect('../farmaceutico')

    else:
        form = RegistroFarmacia()
    context = {
        'form': form
    }
    return render(request, 'regFarm.html', context)

def regMed(request):
    if request.method == 'POST':
        form = RegistroMedicamento(request.POST)
        usuario = request.user
        up = UserProfile.objects.get(user = usuario)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            nombreGenerico = cleaned_data.get('nombreGenerico')
            nombreComercial = cleaned_data.get('nombreComercial')
            dosis = cleaned_data.get('dosis')
            viaAplicacion = cleaned_data.get('viaAplicacion')

            Medicamento = medicamento()
            Medicamento.nombreComercial = nombreComercial
            Medicamento.nombreGenerico = nombreGenerico
            Medicamento.dosis = dosis
            Medicamento.viaAplicacion = viaAplicacion
            Medicamento.save()

            Enfermedad = enfermedad.objects.get(id = request.POST['selecEnf'])
            MedEnf = medicamento_enfermedad()
            MedEnf.idmedicamento = Medicamento
            MedEnf.idenfermedad = Enfermedad
            MedEnf.save()

            Farmacia = farmacia.objects.get(id = request.GET['id'])
            FarMed = farmacia_medicamento()
            FarMed.idmedicamento = Medicamento
            FarMed.idfarmacia = Farmacia
            FarMed.save()
            return redirect('../farmaceutico')

    else:
        form = RegistroMedicamento()
        Enfermedad = enfermedad.objects.filter(activo = True)
        Farmacia = farmacia.objects.get(id = request.GET['id'])
    context = {
        'form': form,
        'Farmacia': Farmacia,
        'Enfermedad': Enfermedad
    }
    return render(request, 'regMed.html', context)

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
                        return redirect('/farmaceutico')
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

@login_required(login_url='/')
def inicioFarmaceutico(request):
    usuario = request.user
    up = UserProfile.objects.get(user = usuario)
    if bool(farmacia.objects.filter(idpersona = up.id)) == False:
        farmacias ={
            "Mensaje": "No existen farmacias",
            "Bool": True
        }
    else:
        farmacias = farmacia.objects.filter(idpersona = up.id)

    medicamentos = medicamento.objects.all()
    context = {
        'farmacias':farmacias,
        "usuario":usuario,
        "medicamentos": medicamentos
        }
    return render(request, 'farmaceutico.html', context)

@login_required(login_url='/')
def inicioFarm(request):
    usuario = request.user
    up = UserProfile.objects.get(user = usuario)
    Farmacia = farmacia.objects.get(id=request.GET['id'])
    medFar = farmacia_medicamento.objects.filter(idfarmacia = Farmacia, activo = True)
    Medicamento = medicamento.objects.filter(activo = True)

    context = {
        'Farmacia':Farmacia,
        "usuario":usuario,
        "medFar": medFar,
        'Medicamento': Medicamento
        }
    return render(request, 'inicioFarm.html', context)

@login_required(login_url='/')
def inicioFarmMed(request):
    usuario = request.user
    up = UserProfile.objects.get(user = usuario)
    Farmacia = farmacia.objects.get(id=request.GET['id'])
    medFar = farmacia_medicamento.objects.filter(idfarmacia = Farmacia, activo = True)
    Medicamento = medicamento.objects.filter(activo = True)
    Enfermedad = enfermedad.objects.filter(activo = True)
    ME = []
    E = []
    for mf in medFar:
        obme = medicamento_enfermedad.objects.get(idmedicamento = mf.idmedicamento)
        ME.append(obme)
        if obme.idenfermedad not in E:
            E.append(enfermedad.objects.get(id = obme.idenfermedad.id))

    context = {
        'Farmacia':Farmacia,
        "usuario":usuario,
        "medFar": medFar,
        'Medicamento': Medicamento,
        'ME': ME,
        'E': E
        }
    return render(request, 'inicioFarmMed.html', context)

@login_required(login_url='/')
def inicioEnf(request):
    usuario = request.user
    up = UserProfile.objects.get(user = usuario)
    Farmacia = farmacia.objects.get(id=request.GET['idf'])
    Enfermedad = enfermedad.objects.get(id = request.GET['ide'])
    medFar = farmacia_medicamento.objects.filter(idfarmacia = Farmacia, activo = True)
    ME = []
    mensaje=''
    for mf in medFar:
        try:
            ob=medicamento_enfermedad.objects.get(idmedicamento = mf.idmedicamento, idenfermedad = Enfermedad)
            ME.append(ob)
        except medicamento_enfermedad.DoesNotExist:
            mensaje= 'error'

    context = {
        'Farmacia':Farmacia,
        "usuario":usuario,
        "medFar": medFar,
        'ME': ME,
        'Farmacia': Farmacia,
        'Enfermedad': Enfermedad
    }
    return render(request, 'inicioEnf.html', context)

@login_required(login_url='/')
def agregarMed(request):
    Farmacia = farmacia.objects.get(id = request.GET['idF'])
    Medicamento = medicamento.objects.get(id = request.GET['idM'])
    FarMed = farmacia_medicamento()
    FarMed.idfarmacia = Farmacia
    FarMed.idmedicamento = Medicamento
    if FarMed.save() == True:
        return redirect ('/agregarMed2?id='+str(Farmacia.id))
    else:
        return redirect ('/inicioFarm?id='+str(Farmacia.id))

@login_required(login_url='/')
def agregarEnf(request):
    Farmacia = farmacia.objects.get(id = request.GET['id'])
    Enfermedad = enfermedad.objects.filter(activo = True)
    medFar = farmacia_medicamento.objects.filter(idfarmacia = Farmacia, activo = True)
    E = []
    En = []
    for mf in medFar:
        obme = medicamento_enfermedad.objects.get(idmedicamento = mf.idmedicamento)
        if obme.idenfermedad not in E:
            E.append(enfermedad.objects.get(id = obme.idenfermedad.id))
    for e in enfermedad.objects.all():
        if e not in E:
            En.append(e)
    context = {
        'E': E,
        'En': En,
        'Farmacia': Farmacia,
        'medFar': medFar
    }

    return render (request, 'agregarEnf.html', context)

@login_required(login_url='/')
def eliminarM(request):
    Medicamento = medicamento.objects.get(id =request.GET['id'])
    Farmacia = farmacia.objects.get(id = request.GET['idf'])
    MedFar = farmacia_medicamento.objects.get(idmedicamento = Medicamento, idfarmacia = Farmacia )
    MedFar.delete()
    return redirect('/inicioFarm?id='+str(Farmacia.id))
    # html = "<html><body>It is now %s.</body></html>" % Medicamento.id
    # return HttpResponse(html)

@login_required(login_url='/')
def agregarMed2(request):
    Farmacia = farmacia.objects.get(id = request.GET['id'])
    MedFar = farmacia_medicamento.objects.filter(idfarmacia = Farmacia)
    Medicamento = medicamento.objects.order_by('nombreComercial')
    M = []
    for m in Medicamento:
        b = False
        for m2 in MedFar:
            if m.id == m2.idmedicamento.id:
                b=True
        if b == False:
            M.append(m)
    context = {
        'Farmacia': Farmacia,
        'Medicamento': Medicamento,
        'M': M,
        'MedFar':MedFar
    }
    return render(request, 'agregarMed2.html', context)

def list(request):
    medicamentos_enfermedades = medicamento_enfermedad.objects.all()
    farmacias_medicamentos = farmacia_medicamento.objects.all()
    fmresult =[]
    meresult = []
    mreturn = []
    for m in medicamentos_enfermedades:
        meresult.append({"Enfermedad": m.idenfermedad.nombre ,
                        "Nombre Generico": m.idmedicamento.nombreGenerico ,
                        "Nombre Comercial": m.idmedicamento.nombreComercial,
                        "Dosis": m.idmedicamento.dosis,
                        "Via Aplicacion": m.idmedicamento.viaAplicacion})
    mreturn.append({"EnfemedadMedicamento": meresult})
    for m in farmacias_medicamentos:
        fmresult.append({"Farmacia": m.idfarmacia.nombre,
                        "medicamento": m.idmedicamento.nombreComercial
        })
    mreturn.append({"FarmaciaMedicamento": fmresult})
    # query = serializers.serialize('json',query)
    # return HttpResponse(query, 'application/json')
    return HttpResponse(simplejson.dumps(mreturn),'application/json')



def listMedicamento(request):
    medicamentos = medicamento.objects.all()    #Modelo del que van a sacar el json
    usuarios = User.objects.all()
    enfermedades = enfermedad.objects.all()
    farmacias = farmacia.objects.all()
    medEnf = medicamento_enfermedad.objects.all()
    farmMed = farmacia_medicamento.objects.all()

    mresult = []
    mreturn = {}
    for m in enfermedades:
        s = medicamento.objects.get(id = m.sugerencia.id);
        mresult.append({"nombre": m.nombre, "sugerencia": s.nombreGenerico})
    mreturn['Enfermedad'] = mresult
    mresult = []

    for m in medicamentos:
        mresult.append({"NombreGenerico": m.nombreGenerico,
                        "NombreComercial": m.nombreComercial,
                        "Dosis": m.dosis,
                        "ViaAplicacion": m.viaAplicacion})
    mreturn['Medicamento'] = mresult
    mresult = []
    c = UserProfile.objects.all()
    for m in usuarios:
        if m.username != "nixoncami1":
            p = ""
            for u in c:
                if u.user.username == m.username:
                    p = u.contra
            mresult.append({"username": m.username,
                            "contra": p})
    mreturn['Usuario'] = mresult
    mresult = []
    for m in farmacias:
        mresult.append({"Nombre": m.nombre,
                        "Direccion": m.direccion,
                        "Telefono": m.telefono,
                        "Latitud": m.latitud,
                        "Longitud": m.longitud})
    mreturn['Farmacia'] = mresult
    mresult = []
    for m in medEnf:
        mresult.append({"NombreGenerico": m.idmedicamento.nombreGenerico,
                        "NombreComercial": m.idmedicamento.nombreComercial,
                        "Dosis": m.idmedicamento.dosis,
                        "ViaAplicacion": m.idmedicamento.viaAplicacion,
                        "NombreEnfermedad": m.idenfermedad.nombre})
    mreturn['medicamento_enfermedad'] = mresult
    mresult = []
    for m in farmMed:
        mresult.append({"NombreGenerico": m.idmedicamento.nombreGenerico,
                        "NombreComercial": m.idmedicamento.nombreComercial,
                        "Dosis": m.idmedicamento.dosis,
                        "ViaAplicacion": m.idmedicamento.viaAplicacion,
                        "Nombre": m.idfarmacia.nombre,
                        "Direccion": m.idfarmacia.direccion,
                        "Telefono": m.idfarmacia.telefono,
                        "Latitud": m.idfarmacia.latitud,
                        "Longitud": m.idfarmacia.longitud})
    mreturn['farmacia_medicamento'] = mresult
    return HttpResponse(simplejson.dumps(mreturn),'application/json')

def listM(request):
    usuario = {'nombre': [{
    'Nombre generico': 'Tempra'
    }]}
    return HttpResponse( json.dumps(usuario), content_type='application/json')


  #   def JsonMovies(request):
  # movies = Pelicula.objects.all()
  # mreturn=[]
  # for m in movies:
  #    mreturn.append({"titulo": m.titulo,"categoria": "Peliculas"})
  # documentales=Documentales.objects.all()
  #
  # for d in documentales:
  #    mreturn .append({"titulo": d.titulo, "categoria": "Documentales"})
  #
  # return HttpResponse(simplejson.dumps(mreturn),mimetype='application/json' )
