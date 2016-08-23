from django import forms
from django.contrib.auth.models import User
from .models import farmacia, medicamento, farmacia_medicamento

t_p =(
("cliente", "Cliente"),
("farmaceutico", "Farmaceutico"),
)

class RegistroMedicamentoFarmacia(forms.ModelForm):
    class Meta:
        model = farmacia_medicamento
        fields = ["idfarmacia","idmedicamento"]

class RegistroFarmacia(forms.ModelForm):
    class Meta:
        model = farmacia
        fields = ["nombre","direccion","telefono","latitud","longitud"]

class RegistroMedicamento(forms.Form):

    nombreComercial= forms.CharField(max_length=40)
    nombreGenerico= forms.CharField(max_length=50)
    dosis= forms.CharField(max_length=20)
    viaAplicacion = forms.CharField(max_length = 40)

    def clean_nombreComercial(self):
        nombreComercial = self.cleaned_data['nombreComercial']
        if medicamento.objects.filter(nombreComercial=nombreComercial):
            raise forms.ValidationError('Nombre de medicamento ya existe.')
        return nombreComercial

class RegistroUserForm(forms.Form):

    username = forms.CharField(min_length = 5)
    email = forms.EmailField()
    password = forms.CharField(min_length = 5, widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    nombre = forms.CharField(max_length = 40)
    apellido = forms.CharField(max_length = 40)
    direccion = forms.CharField(max_length = 200)
    tipo = forms.ChoiceField(choices=t_p)
    edad = forms.IntegerField()
    peso = forms.DecimalField(max_digits = 5, decimal_places = 2)
    telefono = forms.CharField(max_length = 10)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Email ya existe.')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contrasenias no coinciden.')
        return password2
