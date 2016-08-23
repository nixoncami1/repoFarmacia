from django.contrib import admin

# Register your models here.
from .models import UserProfile, enfermedad, farmacia, medicamento, persona_enfermedad, medicamento_enfermedad, farmacia_medicamento, farmacia_persona

class AdminEnfermedad(admin.ModelAdmin):
    list_display = ["__str__", "nombre", "sugerencia"]
    class Meta:
        model = enfermedad

class AdminFarmacia(admin.ModelAdmin):
    list_display = ["__str__", 'nombre', 'direccion', 'telefono', 'latitud', 'longitud']
    class Meta:
        model = farmacia

class AdminMedicamento(admin.ModelAdmin):
    list_display = ["__str__", 'nombreComercial', 'nombreGenerico', 'dosis', 'viaAplicacion']
    class Meta:
        model = medicamento

class AdminPersonaEnfermedad(admin.ModelAdmin):
    list_display = ["__str__", 'idpersona', 'idenfermedad', 'fecha']
    class Meta:
        model = persona_enfermedad

class AdminMedicamentoEnfermedad(admin.ModelAdmin):
    list_display = ["__str__", 'idmedicamento', 'idenfermedad']
    class Meta:
        model = medicamento_enfermedad

class AdminFarmaciaMedicamento(admin.ModelAdmin):
    list_display = ["__str__", 'idfarmacia', 'idmedicamento']
    class Meta:
        model = farmacia_medicamento

class AdminFarmaciaPersona(admin.ModelAdmin):
    list_display = ["__str__", 'idpersona', 'idfarmacia']
    class Meta:
        model = farmacia_persona


admin.site.register(UserProfile)
admin.site.register(enfermedad, AdminEnfermedad)
admin.site.register(farmacia, AdminFarmacia)
admin.site.register(medicamento, AdminMedicamento)
admin.site.register(persona_enfermedad, AdminPersonaEnfermedad)
admin.site.register(medicamento_enfermedad, AdminMedicamentoEnfermedad)
admin.site.register(farmacia_medicamento, AdminFarmaciaMedicamento)
admin.site.register(farmacia_persona, AdminFarmaciaPersona)
