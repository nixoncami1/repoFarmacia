from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registro/$', views.registro_usuario_view, name='registro'),
    url(r'^cliente/$', views.listarProductos, name='cliente'),
    url(r'^farmaceutico/$', views.inicioFarmaceutico, name='farmaceutico'),
    url(r'^regFarm/$', views.regFarm, name='regFarm'),
    url(r'^inicioFarm/$', views.inicioFarm, name='inicioFarm'),
    url(r'^inicioFarmMed/$', views.inicioFarmMed, name='inicioFarmMed'),
    url(r'^agregarMedEnfFarm/$', views.agregarMedEnfFarm, name='agregarMedEnfFarm'),
    url(r'^agregarMedEnfFarmPass/$', views.agregarMedEnfFarmPass, name='agregarMedEnfFarmPass'),
    url(r'^agregarMedEnfFarmNuevo/$', views.agregarMedEnfFarmNuevo, name='agregarMedEnfFarmNuevo'),
    url(r'^inicioEnf/$', views.inicioEnf, name='inicioEnf'),
    url(r'^regMed/$', views.regMed, name='regMed'),
    url(r'^agregarMed/$', views.agregarMed, name='agregarMed'),
    url(r'^agregarEnf/$', views.agregarEnf, name='agregarEnf'),
    url(r'^eliminarM/$', views.eliminarM, name='eliminarM'),
    url(r'^eliminarME/$', views.eliminarME, name='eliminarME'),
    url(r'^agregarMed2/$', views.agregarMed2, name='agregarMed2'),
    url(r'^listarMedicamento/$', views.listarMedicamento),
    url(r'^listarFarmacia/$', views.listarFarmacias),
    url(r'^salir/$', views.salir),
    url(r'^list/$', 'appF.views.list'),
    url(r'^listMe/$', 'appF.views.listM'),
    url(r'^listM/$', 'appF.views.listMedicamento'),
]
