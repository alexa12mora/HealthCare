from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import *
from admin_datta.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CustomRegistrationForm(RegistrationForm):
    password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
      label=_("Confirm Password"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    USER_TYPE_CHOICES = (
        ('medico', 'Médico'),
        ('secretaria', 'Secretaria')
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    class Meta:
        model = User
        fields = ('username', 'email', )

        widgets = {
        'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        'email': forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['Nombre', 'correo']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class CostosPorAsistenteForm(forms.ModelForm):
    class Meta:
        model = CostosPorAsistente
        fields = ['TipoAsistente', 'MontoCosto']
        widgets = {
            'TipoAsistente': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoCosto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AsistentesForm(forms.ModelForm):
    class Meta:
        model = Asistentes
        fields = ['Nombre', 'correo', 'CodCostoPorAsistente']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'CodCostoPorAsistente': forms.Select(attrs={'class': 'form-control'}),
        }

class EmisorForm(forms.ModelForm):
    class Meta:
        model = Emisor
        fields = ['NombreBanco']
        widgets = {
            'NombreBanco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AseguradorasForm(forms.ModelForm):
    class Meta:
        model = Aseguradoras
        fields = ['NombreAseguradora']
        widgets = {
            'NombreAseguradora': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CostosDeOperacionesForm(forms.ModelForm):
    class Meta:
        model = CostosDeOperaciones
        fields = ['NombreOperacion', 'MontoCosto']
        widgets = {
            'NombreOperacion': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoCosto': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class serviciosForm(forms.ModelForm):
    class Meta:
        model = servicios
        fields = ['Fecha', 'TipoCirugia', 'Hospital', 'NombrePaciente', 'MontoTotal', 'MedioPago', 'CodAseguradora', 'CodBanco', 'EstadoPago', 'codMedico', 'CodCostoOperacion', 'CodAsistente', 'DescripcionProcedimiento', 'numFactura']
        widgets = {
            'Fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'TipoCirugia': forms.TextInput(attrs={'class': 'form-control'}),
            'Hospital': forms.TextInput(attrs={'class': 'form-control'}),
            'NombrePaciente': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoTotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'MedioPago': forms.TextInput(attrs={'class': 'form-control'}),
            'CodAseguradora': forms.Select(attrs={'class': 'form-control'}),
            'CodBanco': forms.Select(attrs={'class': 'form-control'}),
            'EstadoPago': forms.TextInput(attrs={'class': 'form-control'}),
            'codMedico': forms.Select(attrs={'class': 'form-control'}),
            'CodCostoOperacion': forms.Select(attrs={'class': 'form-control'}),
            'CodAsistente': forms.Select(attrs={'class': 'form-control'}),
            'DescripcionProcedimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'numFactura': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FacturasForm(forms.ModelForm):
    class Meta:
        model = Facturas
        fields = ['FechaPago', 'CodProcedimiento']
        widgets = {
            'FechaPago': forms.DateInput(attrs={'class': 'form-control'}),
            'CodProcedimiento': forms.Select(attrs={'class': 'form-control'}),
        }

class FacturasAsistentesForm(forms.ModelForm):
    class Meta:
        model = FacturasAsistentes
        fields = ['FechaEmision', 'CodAsistente', 'CodProcedimiento', 'descFactura']
        widgets = {
            'FechaEmision': forms.DateInput(attrs={'class': 'form-control'}),
            'CodAsistente': forms.Select(attrs={'class': 'form-control'}),
            'CodProcedimiento': forms.Select(attrs={'class': 'form-control'}),
            'descFactura': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PagosAsistentesForm(forms.ModelForm):
    class Meta:
        model = PagosAsistentes
        fields = ['CodOperacion', 'CodAsistente', 'MontoPagado', 'FechaPago']
        widgets = {
            'CodOperacion': forms.Select(attrs={'class': 'form-control'}),
            'CodAsistente': forms.Select(attrs={'class': 'form-control'}),
            'MontoPagado': forms.NumberInput(attrs={'class': 'form-control'}),
            'FechaPago': forms.DateInput(attrs={'class': 'form-control'}),
        }

# class PerfilesDeAccesoForm(forms.ModelForm):
#     class Meta:
#         model = PerfilesDeAcceso
#         fields = ['NombreUsuario', 'Password', 'TipoUsuario', 'NivelDeAcceso']
#         widgets = {
#             'NombreUsuario': forms.TextInput(attrs={'class': 'form-control'}),
#             'Password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'TipoUsuario': forms.Select(attrs={'class': 'form-control'}),
#             'NivelDeAcceso': forms.NumberInput(attrs={'class': 'form-control'}),
#         }

