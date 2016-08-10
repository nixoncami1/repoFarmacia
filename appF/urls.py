from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registro/$', views.registro_usuario_view, name='registro'),
    url(r'^cliente/$', views.listarProductos, name='cliente'),
    url(r'^listarMedicamento/$', views.listarMedicamento),
    url(r'^listarFarmacia/$', views.listarFarmacias),
    url(r'^salir/$', views.salir),
]
