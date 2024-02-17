from datetime import date
from django import forms
from django.contrib.auth.models import User
from django import forms
from .models import *
from admin_datta.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django import forms
from .models import servicios, Aseguradoras, Emisor, Medico, CostosDeOperaciones
from datetime import date


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
class CustomLoginForm(AuthenticationForm):
    username = UsernameField(label=_("Your Username"), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}))
    password = forms.CharField(
      label=_("Your Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Contraseña"}),
  )
    
class CustomRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}),
    )
    USER_TYPE_CHOICES = (
        ('medico', 'Médico'),
        ('secretaria', 'Secretaria')
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(),required=False,label="Escoge al médico", widget=forms.Select(attrs={'class': 'form-control', 'id': 'medico'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','user_type', 'medico' )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico'
            })
            
        }
        
class CustomUserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Correo electrónico'
    }))
   
 
class CustomUserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nueva contraseña'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'
    }), label="Confirm New Password")
        
class CustomUserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Contraseña anterior'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nueva contraseña'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'
    }), label="Confirm New Password")        
    
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
        fields = ['TipoAsistente', 'MontoCosto','codMedico']
        widgets = {
            'TipoAsistente': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoCosto': forms.NumberInput(attrs={'class': 'form-control'}),
            'codMedico': forms.HiddenInput(), 
        }
        


class AsistentesForm2(forms.ModelForm):
    class Meta:
        model = Asistentes
        fields = ['Nombre', 'correo']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control nombreasistente', 'required': False,'readonly': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),   
        }    
     

class AsistentesForm(forms.ModelForm):
    class Meta:
        model = Asistentes
        fields = ['CodCostoPorAsistente','Nombre', 'correo', 'monto']
        labels = {
            'CodCostoPorAsistente': 'Tipo asistente',
            'Nombre': 'Nombre',
            'correo': 'Correo electrónico ',
            'monto': 'Monto asociado',
        }
        widgets = {
            'CodCostoPorAsistente': forms.Select(attrs={'class': 'form-control codcostoporasistente'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),   
            'monto': forms.NumberInput(attrs={'class': 'form-control monto'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # obtén el usuario actual
        super(AsistentesForm, self).__init__(*args, **kwargs)
        self.fields['CodCostoPorAsistente'].queryset = CostosPorAsistente.objects.filter(codMedico=user)  # filtra por el usuario actual

        # Aquí es donde estableces las opciones para el campo 'Nombre'
        if self.instance and self.instance.pk: 
            self.fields['Nombre'].queryset = Asistentes.objects.filter(pk=self.instance.pk)
            self.fields['Nombre'].widget = forms.TextInput(attrs={'class': 'form-control nombreasistente'})
        else:
            print("ENTRA AL QUE NO TIENE INSTANCIA VAICA ")
            self.fields['Nombre'].widget = forms.Select(attrs={'class': 'form-control nombreasistente'})



AsistentesFormSet = forms.inlineformset_factory(
    servicios,
    Asistentes,
    form=AsistentesForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)



class EmisorForm(forms.ModelForm):
    class Meta:
        model = Emisor
        fields = ['NombreBanco','codMedico']
        widgets = {
            'NombreBanco': forms.TextInput(attrs={'class': 'form-control'}),
            'codMedico': forms.HiddenInput(), 
        }

class AseguradorasForm(forms.ModelForm):
    class Meta:
        model = Aseguradoras
        fields = ['NombreAseguradora', 'codMedico']  # Agrega 'codMedico' al formulario
        widgets = {
            'NombreAseguradora': forms.TextInput(attrs={'class': 'form-control'}),
            'codMedico': forms.HiddenInput(), 
        }

class HospitalesForm(forms.ModelForm):
    class Meta:
        model = Hospitales
        fields = ['NombreHospital','codMedico']
        widgets = {
            'NombreHospital': forms.TextInput(attrs={'class': 'form-control'}),
            'codMedico': forms.HiddenInput(), 
        }
                
class CostosDeOperacionesForm(forms.ModelForm):
    class Meta:
        model = CostosDeOperaciones
        fields = ['NombreOperacion', 'MontoCosto','codMedico']
        widgets = {
            'NombreOperacion': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoCosto': forms.NumberInput(attrs={'class': 'form-control'}),
            'codMedico': forms.HiddenInput(),
            
        }

class serviciosForm(forms.ModelForm):
    CodAseguradora = forms.ModelChoiceField(queryset=Aseguradoras.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    CodBanco = forms.ModelChoiceField(queryset=Emisor.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    codMedico = forms.ModelChoiceField(queryset=Medico.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    CodCostoOperacion = forms.ModelChoiceField(queryset=CostosDeOperaciones.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    MedioPago = forms.ChoiceField(choices=(('', 'Seleccione'), ('Contado', 'Contado'), ('Credito', 'Crédito')), widget=forms.Select(attrs={'class': 'form-control'}))
    EstadoPago = forms.ChoiceField(
        choices=(('', 'Seleccione'), ('Pagada', 'Pagada'), ('Pendiente', 'Pendiente')),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    CodHospital = forms.ModelChoiceField(queryset=Hospitales.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = servicios
        fields = ['Fecha', 'NombrePaciente', 'MontoTotal', 'MedioPago', 'CodAseguradora', 'CodBanco','CodHospital', 'EstadoPago', 'codMedico', 'CodCostoOperacion', 'numFactura']
        widgets = {
            'Fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'NombrePaciente': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoTotal': forms.NumberInput(attrs={'class': 'form-control'}),
            'numFactura': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_numFactura'}),
            'MedioPago': forms.Select(attrs={'class': 'form-control', 'id': 'forma-pago'}), 
        }
        
    def __init__(self, user, *args, **kwargs):
        super(serviciosForm, self).__init__(*args, **kwargs)
        fecha_actual = date.today()
        self.fields['Fecha'].initial = fecha_actual  
        self.fields['numFactura'].initial = '1'
        if self.instance and self.instance.Fecha:
            # Formatea la fecha al formato 'YYYY-MM-DD'
           self.initial['Fecha'] = self.instance.Fecha.strftime('%Y-%m-%d')

        if user.is_authenticated:
            if Medico.objects.filter(correo=user.email).exists():
                medico = Medico.objects.get(correo=user.email)
            elif Secretaria.objects.filter(correo=user.email).exists():
                secretaria = Secretaria.objects.get(correo=user.email)
                medico = Medico.objects.get(codMedico=secretaria.medico_id)
  # Redirige a una página de error si el usuario no es ni médico ni secretaria
            self.fields['codMedico'].queryset = Medico.objects.filter(codMedico=medico.codMedico)
            self.fields['CodAseguradora'].queryset = Aseguradoras.objects.filter(codMedico=medico.codMedico)
            self.fields['CodBanco'].queryset = Emisor.objects.filter(codMedico=medico.codMedico)
            self.fields['CodCostoOperacion'].queryset = CostosDeOperaciones.objects.filter(codMedico=medico.codMedico)
            self.fields['CodHospital'].queryset = Hospitales.objects.filter(codMedico=medico.codMedico)
            if self.instance.EstadoCierre:
                for field_name, field in self.fields.items():
                    field.widget.attrs['disabled'] = True
                    
                    

class FacturasForm(forms.ModelForm):
    class Meta:
        model = Facturas
        fields = ['FechaPago', 'NumeroFactura']
        widgets = {
            'FechaPago': forms.DateInput(attrs={'class': 'form-control','placeholder': 'Formato: dd/mm/yyyy','type': 'date'}),
            'NumeroFactura': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(FacturasForm, self).__init__(*args, **kwargs)
        self.fields['FechaPago'].required = False
        self.fields['NumeroFactura'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        fecha_pago = cleaned_data.get("FechaPago")
        if fecha_pago is None:
            cleaned_data['FechaPago'] = None
  
    
class FacturasAsistentesForm(forms.ModelForm):
    class Meta:
        model = FacturasAsistentes
        fields = ['FechaEmision','descFactura']
        widgets = {
            'FechaEmision': forms.DateInput(attrs={'class': 'form-control','placeholder': 'Formato: dd/mm/yyyy','type': 'date'}),
            'descFactura': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el campo FechaEmision con la fecha actual
        fecha_actual = date.today().strftime('%Y-%m-%d')
        self.fields['FechaEmision'].initial = fecha_actual  
        
        if self.instance.estado:
            for field in self.fields.values():
                field.disabled = True
                
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get("FechaEmision")
        if fecha_emision is None:
            cleaned_data['FechaEmision'] = None
        desc_factura = cleaned_data.get("descFactura")
        if not desc_factura:
            cleaned_data['descFactura'] = None

        return cleaned_data

        
class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['FechaReporte', 'Servicios', 'Medico', 'Asistente']
        widgets = {
            'FechaReporte': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'Servicios': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'Medico': forms.Select(attrs={'class': 'form-control'}),
            'Asistente': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from datetime import date

class CobrosForm(forms.ModelForm):
    class Meta:
        model = Cobros
        fields = ['FechaCreacion', 'NombreDelCliente', 'NombrepacienteAsociado', 'MontoCobrar', 'TipoCirugia','FechaPago','numReferenciaBanco']
        widgets = {
            'FechaCreacion': forms.DateInput(attrs={'class': 'form-control','type': 'date','required': True}),           
            'NombreDelCliente': forms.Select(attrs={'class': 'form-control', 'id': 'nombre_cliente_select'}),
            'NombrepacienteAsociado': forms.TextInput(attrs={'class': 'form-control'}),
            'MontoCobrar': forms.NumberInput(attrs={'class': 'form-control'}),
            'TipoCirugia': forms.Select(attrs={'class': 'form-control', 'id': 'nombre_servicio_select'}),
            'FechaPago': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numReferenciaBanco': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self,user, *args, **kwargs):
        super(CobrosForm, self).__init__(*args, **kwargs)
        fecha_actual = date.today()
        self.fields['FechaCreacion'].initial = fecha_actual  
        self.fields['FechaPago'].initial = fecha_actual  
        if self.instance and self.instance.FechaCreacion:
            # Formatea la fecha al formato 'YYYY-MM-DD'
           self.initial['FechaCreacion'] = self.instance.FechaCreacion.strftime('%Y-%m-%d')
        if self.instance and self.instance.FechaPago:
            # Formatea la fecha al formato 'YYYY-MM-DD'
           self.initial['FechaPago'] = self.instance.FechaPago.strftime('%Y-%m-%d')
        
        
        if user.is_authenticated:  
            if Medico.objects.filter(correo=user.email).exists():
                medico = Medico.objects.get(correo=user.email)
            elif Secretaria.objects.filter(correo=user.email).exists():
                secretaria = Secretaria.objects.get(correo=user.email)
                medico = Medico.objects.get(codMedico=secretaria.medico_id)
         
            # Obtener los nombres únicos de los asistentes del médico actual
            nombres_asistentes = Asistentes.objects.filter(servicio__codMedico=medico.codMedico).values_list('Nombre', flat=True).distinct('correo')

            # Crear una lista de opciones para el campo NombreDelCliente
            opciones_cliente = [(nombre, nombre) for nombre in nombres_asistentes]

            # Agregar la opción "Agregar Nuevo" a la lista de opciones
            opciones_cliente.append(('Agregar Nuevo', 'Agregar Nuevo'))

            # Actualizar las opciones del campo NombreDelCliente en el widget
            self.fields['NombreDelCliente'].widget.choices = opciones_cliente

            # Obtener los nombres únicos de los servicios del médico actual
            nombre_operaciones = servicios.objects.filter(codMedico=medico.codMedico).values_list('CodCostoOperacion__NombreOperacion', flat=True).distinct()

            # Crear una lista de opciones para el campo TipoCirugia
            opciones_servicios = [(nombre, nombre) for nombre in nombre_operaciones]

            # Agregar la opción "Agregar Nuevo" a la lista de opciones
            opciones_servicios.append(('Agregar Nuevo', 'Agregar Nuevo'))

            # Actualizar las opciones del campo TipoCirugia en el widget
            self.fields['TipoCirugia'].widget.choices = opciones_servicios