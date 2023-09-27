import datetime
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
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .forms import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from datetime import datetime
from django.contrib.auth import get_user_model

def index(request):
  users = User.objects.all()
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
            medico = form.cleaned_data['medico']
            Secretaria.objects.create(codSecretaria=self.object.id,Nombre=self.object.username, correo=self.object.email, medico=medico)
        return response
      
class UserLoginView(LoginView):
    template_name = 'accounts/auth-signin.html'
    form_class = CustomLoginForm

    def form_invalid(self, form):
        if self.request.POST.get('username'):
            username = self.request.POST.get('username')
            user = User.objects.filter(username=username).first()
            if user and not user.is_active:  
                form.errors.clear()         
                form.add_error(None, 'Usuario no está activo.')
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
          return redirect('profile')
          
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
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    insurers = Aseguradoras.objects.all()
    if request.method == 'POST':
        form = AseguradorasForm(request.POST)
        if form.is_valid():
            aseguradora = form.save(commit=False)
            aseguradora.codMedico = user
            aseguradora.save()
            return redirect('listar_aseguradoras')
    else:
        form = AseguradorasForm()
    context = {
        'insurers': insurers,
        'segment': 'add_insurer',
        'form': form,
    }
    
    return render(request, 'medical_reports/insurers/list_insurers.html', context)


@login_required(login_url='/accounts/login/')
def update_insurer(request, pk):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    aseguradora = get_object_or_404(Aseguradoras, pk=pk)
    if request.method == 'POST':
        form = AseguradorasForm(request.POST, instance=aseguradora)
        if form.is_valid():
            aseguradora = form.save(commit=False)
            aseguradora.codMedico = user
            aseguradora.save()
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
    if not Medico.objects.filter(correo=request.user.email).exists():
        return redirect('servicios')
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    insurers = Aseguradoras.objects.filter(codMedico=user.id)
    form = AseguradorasForm()  
    context = {
        'segment': 'Lista_de_aseguradoras',
        'insurers': insurers,
        'form': form,  
    }
    return render(request, 'medical_reports/insurers/list_insurers.html', context)

# Vistas para los hospitales
@login_required(login_url='/accounts/login/')    
def create_hospital(request):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    hospitals = Hospitales.objects.all()
    if request.method == 'POST':
        form = HospitalesForm(request.POST)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.codMedico = user
            hospital.save()
            return redirect('list_hospital')
    else:
        form = HospitalesForm()
    context = {
        'hospitals': hospitals,
        'segment': 'Agregar_hospital',
        'form': form,
    }
    
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)


@login_required(login_url='/accounts/login/')
def update_hospital(request, pk):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    hospital = get_object_or_404(Hospitales, pk=pk)
    if request.method == 'POST':
        form = HospitalesForm(request.POST, instance=hospital)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.codMedico = user
            hospital.save()
            return redirect('list_hospital')
    else:
        form = HospitalesForm(instance=hospital)

    context = {
        'form': form,
    }

    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)


@login_required(login_url='/accounts/login/')
def list_hospital(request):
    if not Medico.objects.filter(correo=request.user.email).exists():
        return redirect('servicios')
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    hospital = Hospitales.objects.filter(codMedico=user.id)  
    form = HospitalesForm()  
    context = {
        'segment': 'Lista_de_hospitales',
        'hospital': hospital,
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
   
 #Emisores
@login_required(login_url='/accounts/login/')    
def add_emitters(request):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    emisores = Emisor.objects.all()
    if request.method == 'POST':
        form = EmisorForm(request.POST)
        if form.is_valid():
            emisor = form.save(commit=False)
            emisor.codMedico = user
            emisor.save()
            return redirect('list_emisores')
    else:
        form = EmisorForm()
    context = {
        'emisores': emisores,
        'segment': 'emisores',
        'form': form,
        'action': 'Actualizar',
    }
    
    return render(request, 'medical_reports/emitters/list_emitters.html', context)


@login_required(login_url='/accounts/login/')
def list_emitters(request):
    if not Medico.objects.filter(correo=request.user.email).exists():
        return redirect('servicios')
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    emisores = Emisor.objects.filter(codMedico=user.id)  # Obtener todos los Emisores
    form = EmisorForm()  # Crea una instancia del formulario vacío
    context = {
        'segment': 'Lista_de_emisores',
        'emisores': emisores,
        'form': form,
    }
    
    return render(request, 'medical_reports/emitters/list_emitters.html', context)


@login_required(login_url='/accounts/login/')
def update_emitters(request, pk):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    emisor = get_object_or_404(Emisor, pk=pk)
    if request.method == 'POST':
        form = EmisorForm(request.POST, instance=emisor)
        if form.is_valid():
            emisor = form.save(commit=False)
            emisor.codMedico = user
            emisor.save()
            return redirect('list_emisores')
    else:
        form = EmisorForm(instance=emisor)

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
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costos = CostosPorAsistente.objects.all()
    if request.method == 'POST':
        form = CostosPorAsistenteForm(request.POST)
        if form.is_valid():
            costo = form.save(commit=False)
            costo.codMedico = user
            costo.save()
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
    if not Medico.objects.filter(correo=request.user.email).exists():
        return redirect('servicios')
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costos = CostosPorAsistente.objects.filter(codMedico=user.id)
    form = CostosPorAsistenteForm()
    context = {
        'segment': 'Lista_costos',
        'costos': costos,
        'form': form,
    }
    
    return render(request, 'medical_reports/costos_por_asistente/list_costos.html', context)


@login_required(login_url='/accounts/login/')
def update_costos_asistentes(request, pk):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costo = get_object_or_404(CostosPorAsistente, pk=pk)
    if request.method == 'POST':
        form = CostosPorAsistenteForm(request.POST, instance=costo)
        if form.is_valid():
            costo = form.save(commit=False)
            costo.codMedico = user
            costo.save()
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
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costos = CostosDeOperaciones.objects.all()
    if request.method == 'POST':
        form = CostosDeOperacionesForm(request.POST)
        if form.is_valid():
            costo = form.save(commit=False)
            costo.codMedico = user
            costo.save()
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
    if not Medico.objects.filter(correo=request.user.email).exists():
        return redirect('servicios')
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costos = CostosDeOperaciones.objects.filter(codMedico=user.id)
    form = CostosDeOperacionesForm()
    context = {
        'segment': 'Lista_de_costos',
        'costos': costos,
        'form': form,
    }
    
    return render(request, 'medical_reports/costos_servicios/costos_servicios.html', context)


@login_required(login_url='/accounts/login/')
def update_costos_por_servicio(request, pk):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    costo = get_object_or_404(CostosDeOperaciones, pk=pk)
    if request.method == 'POST':
        form = CostosDeOperacionesForm(request.POST, instance=costo)
        if form.is_valid():
            costo = form.save(commit=False)
            costo.codMedico = user
            costo.save()
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
def descargar_reporte_pdf(request, pk):
    asistente = get_object_or_404(Asistentes, pk=pk)
    servicios_asistente = servicios.objects.filter(asistentes=asistente)

    # Crear un objeto BytesIO para almacenar el contenido del PDF
    buffer = BytesIO()

    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Crear una lista para almacenar los elementos del PDF
    elements = []

    # Crear una tabla para los servicios
    data = []
    for servicio in servicios_asistente:
        data.append([servicio.CodCostoOperacion, servicio.Fecha, servicio.MedioPago, servicio.EstadoPago, servicio.MontoTotal])

    table = Table(data, colWidths=[80, 80, 80, 80, 80])
    
    # Aplicar estilos a la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    # Agregar la tabla al PDF
    elements.append(table)

    # Construir el PDF
    doc.build(elements)

    # Obtener el contenido del buffer y crear la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_{asistente.Nombre}.pdf"'
    response.write(pdf)
    return response

#reporte de servicios pagados por aseguradora
@login_required(login_url='/accounts/login/')
def reporte_por_med_serviciospagados(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        asistentes_servicios_list = obtener_asistentes_servicios(medico.pk)
        for item in asistentes_servicios_list:
            asistente = item['asistente']
            servicios_asistente = item['servicios']
             # Obtener el correo del asistente
            correo_asistente = asistente.correo
            # Verificar si ya existe un reporte para este asistente con estado false
            reporte_existente = Reporte.objects.filter(Asistente__correo=correo_asistente, estado=False).first()
            if reporte_existente:
                # Si existe, añadir los nuevos servicios a este reporte
                for servicio in servicios_asistente:
                    if servicio not in reporte_existente.Servicios.all():
                        # Verificar si ya existe un reporte para este servicio y asistente
                        if not Reporte.objects.filter(Servicios=servicio, Asistente__correo=correo_asistente).exists():
                            servicio.EstadoFactura = True
                            servicio.save()
                            reporte_existente.Servicios.add(servicio)
            else:
                # Si no existe, crear un nuevo reporte para el asistente
                nuevos_servicios = [servicio for servicio in servicios_asistente if not Reporte.objects.filter(Servicios=servicio, Asistente__correo=correo_asistente).exists()]
                if nuevos_servicios:  # Solo crear el reporte si hay nuevos servicios
                    reporte = Reporte(
                        FechaReporte=date.today(),
                        Medico=medico,
                        Asistente=asistente
                    )
                    reporte.save()
                    # Añadir todos los nuevos servicios del asistente al nuevo reporte
                    for servicio in nuevos_servicios:
                        servicio.EstadoFactura = True
                        servicio.save()
                        reporte.Servicios.add(servicio)
                    # Crear una nueva factura para el nuevo reporte
                    factura = FacturasAsistentes(
                        CodReporte=reporte, 
                        estado=False
                    )
                    factura.save()
                    
        return redirect('lista_reportes')
    else:
        pass

    context = {
        'segment': 'Reportes',
        'servicios_list': asistentes_servicios_list,
        'medico': medico,
    }
    return render(request, 'medical_reports/servicios/listadereportes.html', context)

def obtener_asistentes_servicios(medico_pk):
    medico = Medico.objects.get(pk=medico_pk)
    servicios_medico = servicios.objects.filter(codMedico=medico.codMedico)
    asistentes_servicios = {}
    for servicio in servicios_medico:
        # Solo considerar los servicios con EstadoCierre en False
        if not servicio.EstadoCierre:
            if not servicio.EstadoFactura:
                if servicio.MedioPago == 'Credito' and servicio.EstadoPago == 'Pagado':
                    factura = Facturas.objects.filter(CodProcedimiento=servicio).first()
                    if factura and factura.estado:
                        asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                        for asistente in asistentes_servicio:
                            asistente_key = asistente.correo
                            if asistente_key not in asistentes_servicios:
                                asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': [], 'montos': []}
                            asistentes_servicios[asistente_key]['servicios'].append(servicio)
                            asistentes_servicios[asistente_key]['montos'].append(asistente.monto)
                elif servicio.MedioPago == 'Contado' and servicio.EstadoPago == 'Pagado':
                    asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                    for asistente in asistentes_servicio:
                        asistente_key = asistente.correo
                        if asistente_key not in asistentes_servicios:
                            asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': [], 'montos': []}
                        asistentes_servicios[asistente_key]['servicios'].append(servicio)
                        asistentes_servicios[asistente_key]['montos'].append(asistente.monto)
    print(asistentes_servicios)                   
    return list(asistentes_servicios.values())

@login_required(login_url='/accounts/login/')
def lista_reportes(request):
    # Verificar si el usuario es un médico
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        reportes = Reporte.objects.filter(Medico=medico)
        lista_reportes = []
        asistentes_servicios = {}  # Mover esta línea aquí
        for reporte in reportes:
            montototal = 0 
            medico = reporte.Medico
            asistente = reporte.Asistente
            servicios = reporte.Servicios.all()
            for item in servicios:
                montototal += float(item.MontoTotal)
            for servicio in servicios:
                if not servicio.EstadoCierre:
                    asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                    for asistente in asistentes_servicio:
                        asistente_key = asistente.correo
                        if asistente_key not in asistentes_servicios:
                            print(asistente_key)
                            asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': [], 'montos': []}
                        # Verificar si el servicio ya está en la lista de servicios del asistente antes de agregarlo
                        if servicio not in asistentes_servicios[asistente_key]['servicios']:
                            asistentes_servicios[asistente_key]['servicios'].append(servicio)
                            asistentes_servicios[asistente_key]['montos'].append(asistente.monto)
            print("==============================================================================================")
            print(asistentes_servicios)
            reporte_info = {
                'reporte': reporte,
                'medico': medico,
                'asistente': asistentes_servicios[asistente.correo]['asistente'],
                'servicios': asistentes_servicios[asistente.correo]['servicios'],
                'montototal': sum(asistentes_servicios[asistente.correo]['montos']),
            }     
            lista_reportes.append(reporte_info) 
        print("****************************************************")              
        print(asistentes_servicios)
        context = {
            'lista_reportes': lista_reportes,
        }
        return render(request, 'medical_reports/servicios/listadereportes.html', context)
    else:
        pass 


#reporte de servicios no pagados por aseguradora
@login_required(login_url='/accounts/login/')
def reporte_por_med_servicios_no_pagados(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_medico = servicios.objects.filter(codMedico=medico.codMedico)
        asistentes_servicios = {}
        for servicio in servicios_medico:
            if servicio.MedioPago == 'Credito' and servicio.EstadoPago == 'Pendiente':
                factura = Facturas.objects.filter(CodProcedimiento=servicio).first()
                if factura.estado == False:
                    asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                    for asistente in asistentes_servicio:
                        asistente_key = asistente.correo
                        if asistente_key not in asistentes_servicios:
                            asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': [], 'total_monto': 0.0}
                        asistentes_servicios[asistente_key]['servicios'].append(servicio)
                        asistentes_servicios[asistente_key]['total_monto'] += float(asistente.CodCostoPorAsistente.MontoCosto)
            elif servicio.MedioPago == 'Contado' and servicio.EstadoPago == 'Pendiente':
                asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                for asistente in asistentes_servicio:
                    asistente_key = asistente.correo
                    if asistente_key not in asistentes_servicios:
                        asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': [], 'total_monto': 0.0}
                    asistentes_servicios[asistente_key]['servicios'].append(servicio)
                    asistentes_servicios[asistente_key]['total_monto'] += float(asistente.CodCostoPorAsistente.MontoCosto)
        asistentes_servicios_list = list(asistentes_servicios.values())
    else:
        pass

    context = {
        'segment': 'reportes',
        'servicios_list': asistentes_servicios_list,
        'medico': medico,
    }
    return render(request, 'medical_reports/servicios/descargareportesnopagados.html', context)


@login_required(login_url='/accounts/login/')
def reporte_por_med_servicios(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_medico = servicios.objects.filter(codMedico=medico.codMedico)
        asistentes_servicios = {}
        for servicio in servicios_medico:
            if servicio.MedioPago == 'Credito':
                factura = Facturas.objects.filter(CodProcedimiento=servicio).first()
                if factura and factura.estado:
                    asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                    for asistente in asistentes_servicio:
                        asistente_key = asistente.correo
                        if asistente_key not in asistentes_servicios:
                            asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': []}
                        asistentes_servicios[asistente_key]['servicios'].append(servicio)
            elif servicio.MedioPago == 'Contado' and servicio.EstadoPago == 'Pagado':
                asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                for asistente in asistentes_servicio:
                    asistente_key = asistente.correo
                    if asistente_key not in asistentes_servicios:
                        asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': []}
                    asistentes_servicios[asistente_key]['servicios'].append(servicio)
        asistentes_servicios_list = list(asistentes_servicios.values())
        print(asistentes_servicios_list)
    else:
        pass
    context = {
        'segment': 'reportes',
        'servicios_list': asistentes_servicios_list,
        'medico': medico,
    }
    return render(request, 'medical_reports/servicios/descargareportespagados.html', context)


@login_required(login_url='/accounts/login/')
def get_asistentes(request, pk):
    # Obtiene el medico actual
    medico = Medico.objects.get(correo=request.user.email)
    costo_operacion = CostosDeOperaciones.objects.get(CodCostoOperacion=pk)
    # Obtiene todos los servicios que tienen el mismo CodCostoOperacion y son del medico actual
    listservicios = servicios.objects.filter(CodCostoOperacion=costo_operacion, codMedico=medico)
    # Obtiene todos los asistentes de esos servicios
    asistentes = Asistentes.objects.filter(servicio__in=listservicios)
    # Crea un diccionario para almacenar los asistentes únicos
    unique_asistentes = {}
    for asistente in asistentes:
        # Usa el correo del asistente como clave del diccionario
        # Esto garantiza que cada asistente se cuente solo una vez
        unique_asistentes[asistente.correo] = asistente
    # Convierte la lista de asistentes en un formato que pueda ser enviado como respuesta JSON
    asistentes_data = [{'Nombre': a.Nombre, 'correo': a.correo, 'CodCostoPorAsistente': a.CodCostoPorAsistente_id, 'monto': a.monto} for a in unique_asistentes.values()]
    return JsonResponse(asistentes_data, safe=False)


#hay que arreglar que solo se filtren los datos que pertencen al doc, en este casonm la lista de tipos de precoo de asistencia cuando se va crear un asistente
@login_required(login_url='/accounts/login/')
def create_servicio(request):
    User = get_user_model()
    user = request.user
    if Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    if request.method == 'POST':
        form = serviciosForm(user, request.POST)
        formset = AsistentesFormSet(request.POST, form_kwargs={'user': user})
        factura_form = FacturasForm(request.POST)
        if form.is_valid() and formset.is_valid() and factura_form.is_valid():
            print("Si entro")
            servicio = form.save(commit=False)
            # Validar el estado del pago
            if form.cleaned_data['MedioPago'] == 'Credito':
                servicio.EstadoPago = 'Pendiente'
            elif form.cleaned_data['MedioPago'] == 'Contado':
                num_factura = form.cleaned_data['numFactura']
                if num_factura and num_factura.isdigit() and int(num_factura) > 0:
                    servicio.EstadoPago = 'Pagado'
                else:
                    servicio.EstadoPago = 'Pendiente'
            servicio.save()
            formset.instance = servicio
            asistentes_instances = formset.save()
            # Crear la factura si es pago a crédito
            if form.cleaned_data['MedioPago'] == 'Credito':
                factura = factura_form.save(commit=False)
                factura.CodProcedimiento = servicio
                factura.save()
                print("Si se salva el form de factura")     
            return redirect('list_servicios')
        else:
            print(formset.errors)
    else:
        form = serviciosForm(user, initial={'EstadoPago': 'Pendiente'})
        formset = AsistentesFormSet(form_kwargs={'user': user}) 
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
        form = serviciosForm(request.user,request.POST, instance=servicio)
        formset = AsistentesFormSet(request.POST, instance=servicio, form_kwargs={'user': request.user})
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.save()
            formset.save()
            if servicio.MedioPago == 'Credito':
                factura_form = FacturasForm(request.POST, instance=servicio.facturas_set.first())
                if factura_form.is_valid():
                    fecha_pago = factura_form.cleaned_data.get('FechaPago')
                    factura = factura_form.save(commit=False)
                    factura.CodProcedimiento = servicio
                    if fecha_pago:
                       factura.estado = True
                       servicio.EstadoPago = 'Pagado'
                    else:
                       factura.estado = False 
                       servicio.EstadoPago = 'Pendiente'                                         
                    factura.save()
                else:
                    print("Errores en el formulario de facturas")
                    print(factura_form.errors)
                servicio.save()
            elif form.cleaned_data['MedioPago'] == 'Contado':
                if form.cleaned_data['numFactura'] != '0':
                    servicio.EstadoPago = 'Pagado' 
                else:
                    servicio.EstadoPago = 'Pendiente'
                servicio.save()
            return redirect('list_servicios')
        else:
            print("Errores en el formulario de servicios o asistentes")
            print(form.errors)
            print(formset.errors)
    else:
        form = serviciosForm(request.user,instance=servicio)
        asistentes = servicio.asistentes_set.all()
        formset = AsistentesFormSet(instance=servicio, queryset=asistentes, form_kwargs={'user': request.user})   
        factura_form = FacturasForm(instance=servicio.facturas_set.first())
        formset.extra=0
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

def obtener_monto_costo_asistente(request, cod_costo_servicio_id):
    costo_asistente = CostosPorAsistente.objects.get(pk=cod_costo_servicio_id)
    monto_costo = costo_asistente.MontoCosto
    return JsonResponse({'monto': str(monto_costo)})

@login_required(login_url='/accounts/login/')
def actualizar_factura(request, reporte_id):
    reporte = get_object_or_404(Reporte, pk=reporte_id)
    montoTotal = 0
    try:
        factura_asistente = FacturasAsistentes.objects.get(CodReporte=reporte)
    except FacturasAsistentes.DoesNotExist:
        factura_asistente = None  
    # Obtener la lista de servicios y el asistente del reporte
    servicios_reporte = reporte.Servicios.all()
    asistente_reporte = reporte.Asistente
    if request.method == 'POST':
        form = FacturasAsistentesForm(request.POST, instance=factura_asistente)
        if form.is_valid():
            if form.cleaned_data['FechaEmision'] and form.cleaned_data['descFactura']:
                factura_asistente = form.save(commit=False)
                factura_asistente.CodReporte = reporte
                factura_asistente.estado = True 
                factura_asistente.save()
                # Cambiar el estado del reporte asociado
                reporte.estado = True
                reporte.save()
                return redirect('lista_reportes')
            else:
                messages.error(request, 'Para poder actualizar la factura es necesario que indique la fecha y número de factura ')
               
        else:
            print("No entro")
            print(form.errors)
    else:
        form = FacturasAsistentesForm(instance=factura_asistente)
        for item in servicios_reporte:
            montoTotal += item.MontoTotal
            
    print(factura_asistente.estado)
    context = {
        'segment': 'Actualización de factura por asistente',
        'form': form,
        'reporte': reporte,
        'factura_asistente':factura_asistente,
        'servicios_reporte': servicios_reporte,
        'asistente_reporte': asistente_reporte,
        'montoTotal':montoTotal,
    }
    return render(request, 'medical_reports/servicios/update_factura.html', context)



# crear pagos......
@login_required(login_url='/accounts/login/')
def list_servicios_report(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_list = servicios.objects.filter(codMedico=medico.codMedico,EstadoPago='Pagado',EstadoCierre=False)
        for servicio in servicios_list:
            servicio.Fecha = servicio.Fecha.strftime("%d/%m/%Y")
            servicio.asistentes = Asistentes.objects.filter(servicio=servicio)
    else:
        pass
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        servicios_list = servicios_list.filter(Fecha__range=[start_date, end_date])
    formset = AsistentesFormSet(request.POST)
    form = serviciosForm(request.user)
    context = {
        'segment': 'reportes',
        'servicios_list': servicios_list,
        'form': form,
        'formset': formset,
    }
    return render(request, 'medical_reports/servicios/reportes.html', context)


#VISTA DE NUEVOS REPORTES
@login_required(login_url='/accounts/login/')
def list_servicios(request):
    User = get_user_model()
    user = request.user
    if not Medico.objects.filter(correo=request.user.email).exists() and Secretaria.objects.filter(correo=request.user.email).exists():
        secretaria = Secretaria.objects.get(correo=request.user.email)
        user = User.objects.get(email=secretaria.medico.correo)

    medico = Medico.objects.get(correo=user.email)
    servicios_list = servicios.objects.filter(codMedico=medico.codMedico)
    for servicio in servicios_list:
        servicio.Fecha = servicio.Fecha.strftime("%d/%m/%Y")
        servicio.asistentes = Asistentes.objects.filter(servicio=servicio)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        servicios_list = servicios_list.filter(Fecha__range=[start_date, end_date])
    formset = AsistentesFormSet(request.POST)
    form = serviciosForm(user)
    context = {
        'segment': 'reportes',
        'servicios_list': servicios_list,
        'form': form,
        'formset': formset,
    }
    
    return render(request, 'medical_reports/servicios/list_servicios.html', context)



#pagos
@login_required(login_url='/accounts/login/')
def procesar_pagos(request):
    if request.method == 'POST':
        start_date = request.POST.get('rango_fecha_inicio')
        end_date = request.POST.get('rango_fecha_fin')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")   
            if Medico.objects.filter(correo=request.user.email).exists():
                medico = Medico.objects.get(correo=request.user.email)
                reportes = Reporte.objects.filter(Medico=medico, FechaReporte__range=(start_date, end_date), estado=True,EstadoCierre=False) 
                if not reportes :
                    messages.error(request, 'No hay servicios disponibles para pagar')
                for reporte in reportes:
                    monto_pagado = 0
                    servicios_reporte = reporte.Servicios.all()
                    asistente_reporte = reporte.Asistente
                    if not PagosAsistentes.objects.filter(CodReporte=reporte).exists():
                        monto_pagado = sum(servicio.MontoTotal for servicio in servicios_reporte)        
                        # Crear un nuevo registro en la tabla PagosAsistentes
                        pago_asistente = PagosAsistentes(
                            CodReporte=reporte,
                            CodAsistente=asistente_reporte,
                            MontoPagado=monto_pagado,
                            FechaPago=date.today()
                        )
                        reporte.EstadoCierre = True
                        reporte.save()
                        pago_asistente.save()    
                        # Verificar si todos los reportes que contienen cada servicio tienen el EstadoCierre en true
                        for servicio in servicios_reporte:
                            reportes_servicio = Reporte.objects.filter(Servicios=servicio)
                            if all(reporte.EstadoCierre for reporte in reportes_servicio):                        
                                servicio.EstadoCierre = True
                                servicio.save()                                
        return redirect('reportes')                         
        context = {
        'segment': 'reportes',
        'servicios_list':servicios_list,
    }
    return render(request, 'medical_reports/servicios/generarpagos.html', context)
    
@login_required(login_url='/accounts/login/')    
def reporteserviciospagados(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        asistentes = Asistentes.objects.all()
        lista_asistentes = []

        for asistente in asistentes:
            reportes_asistente = Reporte.objects.filter(Asistente__correo=asistente.correo, EstadoCierre=True, Medico=medico)

            if reportes_asistente.exists():
                asistente_existente = any(item['asistente'].correo == asistente.correo for item in lista_asistentes)
                if not asistente_existente:
                    asistente_info = {
                        'asistente': asistente,
                        'reportes': [],
                    }
                    for reporte in reportes_asistente:
                        servicios_reporte = reporte.Servicios.all()
                        pago_asistente = PagosAsistentes.objects.get(CodReporte=reporte)  # Obtener el pago único
                        
                        reporte_info = {
                            'reporte': reporte,
                            'servicios': servicios_reporte,
                            'pago_asistente': pago_asistente,  # Agregar el pago_asistente
                        }
                        asistente_info['reportes'].append(reporte_info)

                    lista_asistentes.append(asistente_info)
        print(lista_asistentes)
        context = {
            'lista_asistentes': lista_asistentes,
        }
        return render(request, 'medical_reports/servicios/reportespagados.html', context)      
    else:
        pass

 
@login_required(login_url='/accounts/login/')
def reporte_utilidad_pagos(request):
    if request.method == 'POST':
        start_date = request.POST.get('rango_fecha_inicio')
        end_date = request.POST.get('rango_fecha_fin')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")   
            if Medico.objects.filter(correo=request.user.email).exists():
                utilidad_total = 0
                medico = Medico.objects.get(correo=request.user.email)
                servicios_info = []
                list_servicios = servicios.objects.filter(codMedico=medico, Fecha__range=(start_date, end_date), EstadoCierre=True)              
                if list_servicios:        
                    for servicio in list_servicios:
                        asistentes = Asistentes.objects.filter(servicio=servicio)
                        costo_total_asistentes = sum(asistente.CodCostoPorAsistente.MontoCosto for asistente in asistentes)
                        utilidad_servicio = servicio.MontoTotal - costo_total_asistentes
                        utilidad_total += utilidad_servicio
                        servicio_info = {
                            'servicio': servicio,
                            'asistentes': asistentes,
                            'utilidad_servicio': utilidad_servicio,
                        }
                        servicios_info.append(servicio_info)
                    servicio_info = {
                            'utilidad_total': utilidad_total,
                    }
                    servicios_info.append(servicio_info)
                else:
                    print("No hay servicios asociados al médico")                
                context = {
                    'segment': 'reportes',
                    'servicios_info': servicios_info,
                    'utilidad_total': utilidad_total,
                }
                return render(request, 'medical_reports/servicios/reporteutilidad.html', context)
        
