from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser

class UserProfile(models.Model):

	t_p =(
	("cliente", "Cliente"),
	("farmaceutico", "Farmaceutico"),
	)

	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	nombre = models.CharField(max_length = 40, blank=True, null=True)
	apellido = models.CharField(max_length = 40, blank=True, null=True)
	direccion = models.CharField(max_length = 200, blank=True, null=True)
	tipo = models.CharField(max_length = 30, choices = t_p)
	edad = models.IntegerField()
	peso = models.DecimalField(max_digits = 5, decimal_places = 2)
	telefono = models.CharField(max_length=15)
	activo = models.BooleanField(default = True)
	contra = models.CharField(max_length = 40, default="")

	def __str__(self):
		return self.user.username

class enfermedad(models.Model):

	nombre = models.CharField(max_length=30)
	sugerencia = models.ForeignKey("medicamento")
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.nombre

class farmacia(models.Model):

	nombre= models.CharField(max_length=30)
	direccion= models.CharField(max_length=200)
	telefono= models.CharField(max_length=10)
	latitud = models.CharField(max_length=30)
	longitud = models.CharField(max_length=30)
	idpersona = models.ForeignKey("UserProfile", null = True)
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.nombre

class medicamento(models.Model):

	nombreComercial= models.CharField(max_length=40)
	nombreGenerico= models.CharField(max_length=50)
	dosis= models.CharField(max_length=20)
	viaAplicacion = models.CharField(max_length = 40)
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.nombreComercial

class persona_enfermedad(models.Model):

	idpersona = models.ForeignKey("UserProfile")
	idenfermedad = models.ForeignKey("enfermedad")
	fecha = models.DateField(blank=True, null=True)
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.idpersona.user.username

class medicamento_enfermedad(models.Model):

	idmedicamento = models.ForeignKey("medicamento")
	idenfermedad = models.ForeignKey("enfermedad")
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.idenfermedad.nombre


class farmacia_medicamento(models.Model):

	idfarmacia = models.ForeignKey("farmacia")
	idmedicamento = models.ForeignKey("medicamento")
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.idmedicamento.nombreComercial

class farmacia_persona(models.Model):
	idpersona = models.ForeignKey("UserProfile")
	idfarmacia = models.ForeignKey("farmacia")
	activo = models.BooleanField(default = True)

	def __str__(self):
		return self.idpersona.nombre
