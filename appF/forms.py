from django import forms
from django.contrib.auth.models import User

t_p =(
("cliente", "Cliente"),
("farmaceutico", "Farmaceutico"),
)

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
