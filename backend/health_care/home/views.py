from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
#from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

def index(request):
  print("Hola")
  users = User.objects.all()
  print(users)
  context = {
    'segment': 'index',
    'users':users,
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/tables.html", context)

# Components
@login_required(login_url='/accounts/login/')
def bc_button(request):
  context = {
    'parent': 'basic_components',
    'segment': 'button'
  }
  return render(request, "pages/components/bc_button.html", context)

@login_required(login_url='/accounts/login/')
def bc_badges(request):
  context = {
    'parent': 'basic_components',
    'segment': 'badges'
  }
  return render(request, "pages/components/bc_badges.html", context)

@login_required(login_url='/accounts/login/')
def bc_breadcrumb_pagination(request):
  context = {
    'parent': 'basic_components',
    'segment': 'breadcrumbs_&_pagination'
  }
  return render(request, "pages/components/bc_breadcrumb-pagination.html", context)

@login_required(login_url='/accounts/login/')
def bc_collapse(request):
  context = {
    'parent': 'basic_components',
    'segment': 'collapse'
  }
  return render(request, "pages/components/bc_collapse.html", context)

@login_required(login_url='/accounts/login/')
def bc_tabs(request):
  context = {
    'parent': 'basic_components',
    'segment': 'navs_&_tabs'
  }
  return render(request, "pages/components/bc_tabs.html", context)

@login_required(login_url='/accounts/login/')
def bc_typography(request):
  context = {
    'parent': 'basic_components',
    'segment': 'typography'
  }
  return render(request, "pages/components/bc_typography.html", context)

@login_required(login_url='/accounts/login/')
def icon_feather(request):
  context = {
    'parent': 'basic_components',
    'segment': 'feather_icon'
  }
  return render(request, "pages/components/icon-feather.html", context)


# Forms and Tables
@login_required(login_url='/accounts/login/')
def form_elements(request):
  context = {
    'parent': 'form_components',
    'segment': 'form_elements'
  }
  return render(request, 'pages/form_elements.html', context)

@login_required(login_url='/accounts/login/')
def basic_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'basic_tables'
  }
  return render(request, 'pages/tbl_bootstrap.html', context)

# Chart and Maps
@login_required(login_url='/accounts/login/')
def morris_chart(request):
  context = {
    'parent': 'chart',
    'segment': 'morris_chart'
  }
  return render(request, 'pages/chart-morris.html', context)

@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/map-google.html', context)

# Authentication
class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = CustomRegistrationForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_active = False
        self.object.save()
        if form.cleaned_data['user_type'] == 'medico':
            Medico.objects.create(codMedico=self.object.id, Nombre=self.object.username, correo=self.object.email)
        else: 
            Secreataria.objects.create(codSecretaria=self.object.id,Nombre=self.object.username, correo=self.object.email)
        return response
      
class UserLoginView(LoginView):
    template_name = 'accounts/auth-signin.html'
    form_class = CustomLoginForm

    def form_invalid(self, form):
        if self.request.POST.get('username'):
            username = self.request.POST.get('username')
            user = User.objects.filter(username=username).first()
            if user and not user.is_active:
                form.add_error(None, 'El usuario no está activo.')
        return super().form_invalid(form)

    def get_success_url(self):
        return '/'

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/auth-reset-password.html'
  form_class = CustomUserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/auth-password-reset-confirm.html'
  form_class = CustomUserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/auth-change-password.html'
  form_class = CustomUserPasswordChangeForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def profile(request):
  user = request.user
  if request.method == 'POST':
      user_form = UserForm(request.POST, instance=user)
      if user_form.is_valid():
          user_form.save()
          messages.success(request, 'Your profile has been updated successfully.')
          return redirect('profile')
      else:
          messages.error(request, 'There was an error. Please check your information.')
  else:
      user_form = UserForm(instance=user)

  context = {
      'segment': 'profile',
      'user_form': user_form,
      'user': user,
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def sample_page(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)


@login_required(login_url='/accounts/login/')
def services(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)

# Vistas para el modelo Medico

@login_required(login_url='/accounts/login/')
def medico_list(request):
    medicos = Medico.objects.all()
    return render(request, 'medical_reports/medico_list.html', {'medicos': medicos})


@login_required(login_url='/accounts/login/')
def medico_detail(request, codMedico):
    medico = get_object_or_404(Medico, codMedico=codMedico)
    return render(request, 'medical_reports/medico_detail.html', {'medico': medico})


@login_required(login_url='/accounts/login/')
def medico_create(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medico_list')
    else:
        form = MedicoForm()
    return render(request, 'medical_reports/medico_form.html', {'form': form})


@login_required(login_url='/accounts/login/')
def medico_update(request, codMedico):
    try:
        medico = Medico.objects.get(codMedico=codMedico)
    except Medico.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_list')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medical_reports/medico_form.html', {'form': form})

@login_required(login_url='/accounts/login/')
def medico_delete(request, codMedico):
    medico = get_object_or_404(Medico, codMedico=codMedico)
    if request.method == 'POST':
        medico.delete()
        return redirect('medico_list')
    return render(request, 'medical_reports/medico_confirm_delete.html', {'medico': medico})
  

# Vistas para las aseguradoras
@login_required(login_url='/accounts/login/')    
def create_insurer(request):
    insurers = Aseguradoras.objects.all()  # Definimos la variable insurers fuera del bloque if
    if request.method == 'POST':
        form = AseguradorasForm(request.POST)
        if form.is_valid():
            print("si")
            form.save()
            return redirect('listar_aseguradoras')
    else:
        print("no")
        form = AseguradorasForm()
    context = {
        'insurers': insurers,
        'segment': 'add_insurer',
        'form': form,
    }
    print(form.errors)
    return render(request, 'medical_reports/insurers/list_insurers.html', context)

@login_required(login_url='/accounts/login/')
def update_insurer(request, pk):
    aseguradora = get_object_or_404(Aseguradoras, pk=pk)
    if request.method == 'POST':
        form = AseguradorasForm(request.POST, instance=aseguradora)
        if form.is_valid():
            form.save()
            return redirect('listar_aseguradoras')
    else:
        form = AseguradorasForm(instance=aseguradora)

    context = {
        'form': form,
    }
    return render(request, 'medical_reports/insurers/update_insurer.html', context)

@login_required(login_url='/accounts/login/')
def eliminar_aseguradora(request, pk):
    aseguradora = get_object_or_404(Aseguradoras, pk=pk)
    if request.method == 'POST':
        aseguradora.delete()
        # Redireccionar a la página que muestra la lista actualizada de aseguradoras
        return redirect('listar_aseguradoras')

    # Si la petición no es POST, simplemente redireccionamos a la lista de aseguradoras
    return redirect('listar_aseguradoras')
  
@login_required(login_url='/accounts/login/')
def list_insurers(request):
    insurers = Aseguradoras.objects.all()
    form = AseguradorasForm()  # Crea una instancia del formulario vacío
    context = {
        'segment': 'Lista_de_aseguradoras',
        'insurers': insurers,
        'form': form,  # Incluye el formulario en el contexto
    }
    return render(request, 'medical_reports/insurers/list_insurers.html', context)
  
 
 
 
# Vistas para los hospitales
@login_required(login_url='/accounts/login/')    
def create_hospital(request):
    hospitals = Hospitales.objects.all()  # Definimos la variable insurers fuera del bloque if
    if request.method == 'POST':
        form = HospitalesForm(request.POST)
        if form.is_valid():
            print("si")
            form.save()
            return redirect('list_hospital')
    else:
        print("no")
        form = HospitalesForm()
    context = {
        'hospitals': hospitals,
        'segment': 'Agregar_hospital',
        'form': form,
    }
    print(form.errors)
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)

@login_required(login_url='/accounts/login/')
def update_hospital(request, pk):
    hospital = get_object_or_404(Hospitales, pk=pk)
    if request.method == 'POST':
        form = HospitalesForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('list_hospital')
    else:
        form = HospitalesForm(instance=hospital)

    context = {
        'form': form,
    }
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)

@login_required(login_url='/accounts/login/')
def eliminar_hospital(request, pk):
    hospital = get_object_or_404(Hospitales, pk=pk)
    if request.method == 'POST':
        hospital.delete()
        return redirect('list_hospital')
    return redirect('list_hospital')
  
@login_required(login_url='/accounts/login/')
def list_hospital(request):
    hospital = Hospitales.objects.all()
    form = HospitalesForm()  
    context = {
        'segment': 'Lista_de_hospitales',
        'hospital': hospital,
        'form': form, 
    }
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)
   
 #Emisores
@login_required(login_url='/accounts/login/')
def emitters(request):
    emisores = Emisor.objects.all()  # Obtener todos los Emisores
    if request.method == 'POST':
        form = EmisorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_emisores')
    else:
        form = EmisorForm()
    context = {
        'emisores': emisores,
        'segment': 'emisores',
        'form': form,
        'action': 'Actualizar',
    }
    print(form.errors)
    return render(request, 'medical_reports/emitters/list_emitters.html', context)
  
  
@login_required(login_url='/accounts/login/')
def list_emitters(request):
    emisores = Emisor.objects.all()  # Obtener todos los Emisores
    form = EmisorForm()  # Crea una instancia del formulario vacío
    context = {
        'segment': 'Lista_de_emisores',
        'emisores': emisores,
        'form': form,  # Incluye el formulario en el contexto
    }
    return render(request, 'medical_reports/emitters/list_emitters.html', context)

@login_required(login_url='/accounts/login/')
def update_emitters(request, pk):
    emisor = get_object_or_404(Emisor, pk=pk)
    if request.method == 'POST':
        form = EmisorForm(request.POST, instance=emisor)
        if form.is_valid():
            form.save()
            return redirect('list_emisores')
    else:
        form = AseguradorasForm(instance=emisor)

    context = {
        'form': form,
        'action': 'Actualizar',
    }

    return render(request, 'medical_reports/emitters/list_emitters.html', context)


@login_required(login_url='/accounts/login/')
def eliminar_emisor(request, pk):
    emisor = get_object_or_404(Emisor, pk=pk)
    if request.method == 'POST':
        emisor.delete()
        # Redireccionar a la página que muestra la lista actualizada de aseguradoras
        return redirect('list_emisores')

    # Si la petición no es POST, simplemente redireccionamos a la lista de aseguradoras
    return redirect('list_emisores')
  

@login_required(login_url='/accounts/login/')  
def get_emisor(request, pk):
    emisor = get_object_or_404(Emisor, pk=pk)
    context = {
        'NombreBanco': emisor.NombreBanco,
    }
    return render(request, 'medical_reports/emitters/list_emitters.html', context)
  
#Pago Asistentes 
@login_required(login_url='/accounts/login/')
def create_costos_asistente(request):
    costos = CostosPorAsistente.objects.all()
    if request.method == 'POST':
        form = CostosPorAsistenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagos_asistentes')
    else:
        form = CostosPorAsistenteForm()
    context = {
        'costos': costos,
        'form': form,
        'segment': 'costos',
    }
    return render(request, 'medical_reports/costos_por_asistente/list_costos.html', context)

@login_required(login_url='/accounts/login/')
def list_costos_asistentes(request):
    costos = CostosPorAsistente.objects.all()
    form = CostosPorAsistenteForm()
    context = {
        'segment': 'Lista_costos',
        'costos': costos,
        'form': form,
    }
    return render(request, 'medical_reports/costos_por_asistente/list_costos.html', context)
  
  
@login_required(login_url='/accounts/login/')
def update_costos_asistentes(request, pk):
    costo = get_object_or_404(CostosPorAsistente, pk=pk)
    if request.method == 'POST':
        form = CostosPorAsistenteForm(request.POST, instance=costo)
        if form.is_valid():
            form.save()
            return redirect('pagos_asistentes')
    else:
        form = CostosPorAsistenteForm(instance=costo)

    context = {
        'form': form,
        'action': 'Actualizar',
    }

    return render(request, 'medical_reports/costos_por_asistente/list_costos.html', context)


@login_required(login_url='/accounts/login/')
def eliminar_costos_asistentes(request, pk):
    costo = get_object_or_404(CostosPorAsistente, pk=pk)
    if request.method == 'POST':
        costo.delete()
        print("Si")
        return redirect('pagos_asistentes')
    print("NO")
    return redirect('pagos_asistentes')


#Costos por servicio(operaciones)
@login_required(login_url='/accounts/login/')
def create_costos_por_servicio(request):
    costos = CostosDeOperaciones.objects.all()
    if request.method == 'POST':
        form = CostosDeOperacionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_servicio')
    else:
        form = CostosDeOperacionesForm()
    context = {
        'costos': costos,
        'form': form,
        'segment': 'costos',
    }
    return render(request, 'medical_reports/costos_servicios/costos_servicios.html', context)

@login_required(login_url='/accounts/login/')
def list_costos_por_servicio(request):
    costos = CostosDeOperaciones.objects.all()
    form = CostosDeOperacionesForm()
    context = {
        'segment': 'Lista_de_costos',
        'costos': costos,
        'form': form,
    }
    return render(request, 'medical_reports/costos_servicios/costos_servicios.html', context)

@login_required(login_url='/accounts/login/')
def update_costos_por_servicio(request, pk):
    costo = get_object_or_404(CostosDeOperaciones, pk=pk)
    if request.method == 'POST':
        form = CostosDeOperacionesForm(request.POST, instance=costo)
        if form.is_valid():
            form.save()
            return redirect('list_servicio')
    else:
        form = CostosDeOperacionesForm(instance=costo)

    context = {
        'form': form,
        'action': 'Actualizar',
    }

    return render(request, 'medical_reports/costos_servicios/costos_servicios.html', context)

@login_required(login_url='/accounts/login/')
def eliminar_costos_por_servicio(request, pk):
    costo = get_object_or_404(CostosDeOperaciones, pk=pk)
    if request.method == 'POST':
        costo.delete()
        return redirect('list_servicio')

    return redirect('list_servicio')
 
#asistentes
@login_required(login_url='/accounts/login/')
def list_asistentes(request):
    asistentes = Asistentes.objects.all()
    form = AsistentesForm()
    context = {
        'segment': 'asistentes',
        'asistentes': asistentes,
        'form': form,
    }
    return render(request, 'asistentes_list.html', context)
  
@login_required(login_url='/accounts/login/')
def create_asistente(request):
    if request.method == 'POST':
        form = AsistentesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_asistentes')
    else:
        form = AsistentesForm()
    context = {
        'segment': 'asistentes',
        'form': form,
    }
    return render(request, 'asistente_form.html', context)
  
@login_required(login_url='/accounts/login/')
def update_asistente(request, pk):
    asistente = get_object_or_404(Asistentes, pk=pk)
    if request.method == 'POST':
        form = AsistentesForm(request.POST, instance=asistente)
        if form.is_valid():
            form.save()
            return redirect('list_asistentes')
    else:
        form = AsistentesForm(instance=asistente)
    context = {
        'segment': 'asistentes',
        'form': form,
    }
    return render(request, 'asistente_form.html', context)
  
  
@login_required(login_url='/accounts/login/')
def delete_asistente(request, pk):
    asistente = get_object_or_404(Asistentes, pk=pk)
    if request.method == 'POST':
        asistente.delete()
        return redirect('list_asistentes')
    context = {
        'segment': 'asistentes',
        'asistente': asistente,
    }
    return render(request, 'asistente_confirm_delete.html', context)
  
  
#servicios
@login_required(login_url='/accounts/login/')
def list_servicios(request):
    servicios_list = servicios.objects.all()
    formset = AsistentesFormSet(request.POST)
    form = serviciosForm()
    context = {
        'segment': 'servicios',
        'servicios_list': servicios_list,
        'form': form,
        'formset': formset,
    }
    return render(request, 'medical_reports/servicios/list_servicios.html', context)

#servicios
@login_required(login_url='/accounts/login/')
def create_servicio(request):
    if request.method == 'POST':
        form = serviciosForm(request.POST)
        formset = AsistentesFormSet(request.POST)
        factura_form = FacturasForm(request.POST)
        if form.is_valid() and formset.is_valid() and factura_form.is_valid():
            servicio = form.save(commit=False)
            servicio.EstadoPago = 'Pendiente'
            servicio.save()
            formset.instance = servicio
            asistentes_instances = formset.save()
            for asistente in asistentes_instances:
                factura_asistente = FacturasAsistentes(CodAsistente=asistente)
                factura_asistente.save()
            if form.cleaned_data['MedioPago'] == 'Credito':
                factura = factura_form.save(commit=False)
                factura.CodProcedimiento = servicio
                factura.save()
                print("Si se salva el form de factura")
            elif form.cleaned_data['MedioPago'] == 'Contado':
                print("es de contado")
                pass
            return redirect('list_servicios')
        else:
            print("Errores en alguno de los formularios:")
            print(form.errors)
            print(formset.errors)
            print(factura_form.errors)
    else:
        form = serviciosForm(initial={'EstadoPago': 'Pendiente'})
        formset = AsistentesFormSet()
        factura_form = FacturasForm()

    context = {
        'segment': 'servicios',
        'form': form,
        'formset': formset,
        'factura_form': factura_form,
        'is_update': False,
        
    }
    return render(request, 'medical_reports/servicios/crear_servicio.html', context)



@login_required(login_url='/accounts/login/')
def update_servicio(request, pk):
    servicio = get_object_or_404(servicios, pk=pk)
    factura_form = None
    if request.method == 'POST':
        form = serviciosForm(request.POST, instance=servicio)
        formset = AsistentesFormSet(request.POST, instance=servicio)
        if form.is_valid() and formset.is_valid():
            servicio = form.save(commit=False)
            servicio.EstadoPago = 'Pendiente'  # Establecer el valor del campo EstadoPago
            servicio.save()
            formset.save()           
            if servicio.MedioPago == 'Credito':
                factura_form = FacturasForm(request.POST, instance=servicio.facturas_set.first())
                if factura_form.is_valid():
                    factura = factura_form.save(commit=False)
                    factura.CodProcedimiento = servicio
                    factura.save()
                else:
                    print(factura_form.errors)  
            return redirect('medical_reports/servicios/crear_servicio.html')
        else:
            print("entro al else")
            print(form.errors)
            print(formset.errors)
    else:
        form = serviciosForm(instance=servicio)
        asistentes = servicio.asistentes_set.all()
        formset = AsistentesFormSet(instance=servicio, queryset=asistentes)
        if servicio.MedioPago == 'Credito':
            factura_form = FacturasForm(instance=servicio.facturas_set.first())       

    context = {
        'segment': 'servicios',
        'form': form,
        'servicio': servicio,
        'formset': formset,
        'factura_form': factura_form,
        'is_update': True,
        
    }
    return render(request, 'medical_reports/servicios/crear_servicio.html', context)



  
@login_required(login_url='/accounts/login/')
def delete_servicio(request, pk):
    servicio = get_object_or_404(servicios, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('list_servicios')
    context = {
        'segment': 'servicios',
        'servicio': servicio,
    }
    return render(request, 'medical_reports/servicios/list_servicios.html', context)

def obtener_monto_costo_servicios(request, cod_costo_operacion_id):
    costo_operacion = CostosDeOperaciones.objects.get(pk=cod_costo_operacion_id)
    monto_costo = costo_operacion.MontoCosto
    return JsonResponse({'monto': str(monto_costo)})

#facturas asistente
def actualizar_factura(request, servicio_id, asistente_id):
    servicio = get_object_or_404(servicios, pk=servicio_id)
    asistente = get_object_or_404(Asistentes, pk=asistente_id)
    try:
        factura_asistente = FacturasAsistentes.objects.get(CodAsistente=asistente)
    except FacturasAsistentes.DoesNotExist:
        factura_asistente = None
    if request.method == 'POST':
        form = FacturasAsistentesForm(request.POST, instance=factura_asistente)
       
        if form.is_valid():
            print("entro")
            factura_asistente = form.save(commit=False)
            factura_asistente.CodAsistente = asistente
            factura_asistente.save()
            return redirect('update_servicio', pk=servicio.pk)
        else:
             print("Noentro")
             print()
            
    else:
        form = FacturasAsistentesForm(instance=factura_asistente)
    context = {
        'form': form,
        'servicio': servicio,
        'asistente': asistente,
    }

    return render(request, 'medical_reports/servicios/update_factura.html', context)
