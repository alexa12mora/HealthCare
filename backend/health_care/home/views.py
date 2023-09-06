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
    insurers = Aseguradoras.objects.all()
    if request.method == 'POST':
        form = AseguradorasForm(request.POST)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
                form.save()
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
    aseguradora = get_object_or_404(Aseguradoras, pk=pk)
    if request.method == 'POST':
        form = AseguradorasForm(request.POST, instance=aseguradora)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    insurers = Aseguradoras.objects.filter(codMedico=request.user.id)
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
    hospitals = Hospitales.objects.all()  # Definimos la variable insurers fuera del bloque if
    if request.method == 'POST':
        form = HospitalesForm(request.POST)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)

@login_required(login_url='/accounts/login/')
def update_hospital(request, pk):
    hospital = get_object_or_404(Hospitales, pk=pk)
    if request.method == 'POST':
        form = HospitalesForm(request.POST, instance=hospital)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    hospital = Hospitales.objects.filter(codMedico=request.user.id)  
    form = HospitalesForm()  
    context = {
        'segment': 'Lista_de_hospitales',
        'hospital': hospital,
        'form': form, 
    }
    return render(request, 'medical_reports/hospitals/list_hospitals.html', context)
   
 #Emisores
@login_required(login_url='/accounts/login/')
def add_emitters(request):
    emisores = Emisor.objects.all()  
    if request.method == 'POST':
        form = EmisorForm(request.POST)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    return render(request, 'medical_reports/emitters/list_emitters.html', context)
  
  
@login_required(login_url='/accounts/login/')
def list_emitters(request):
    emisores = Emisor.objects.filter(codMedico=request.user.id)  # Obtener todos los Emisores
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
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
        print("-----------------",form.errors)
        if form.is_valid():
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    costos = CostosPorAsistente.objects.filter(codMedico=request.user.id)
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
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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
    costos = CostosDeOperaciones.objects.filter(codMedico=request.user.id) 
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
            doctor = Medico.objects.filter(correo=request.user.email).first()
            if doctor:
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

#reporte de servicios no pagados por aseguradora
@login_required(login_url='/accounts/login/')
def reporte_por_med_servicios_no_pagados(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_medico = servicios.objects.filter(codMedico=medico.codMedico)
        asistentes_servicios = {}
        for servicio in servicios_medico:
            if servicio.MedioPago == 'Credito':
                factura = Facturas.objects.filter(CodProcedimiento=servicio).first()
                if factura.estado == False:
                    asistentes_servicio = Asistentes.objects.filter(servicio=servicio)
                    for asistente in asistentes_servicio:
                        asistente_key = asistente.correo
                        if asistente_key not in asistentes_servicios:
                            asistentes_servicios[asistente_key] = {'asistente': asistente, 'servicios': []}
                        asistentes_servicios[asistente_key]['servicios'].append(servicio)
            elif servicio.MedioPago == 'Contado' and servicio.EstadoPago == 'Pendiente':
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
def list_servicios_report(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_list = servicios.objects.filter(codMedico=medico.codMedico)
        for servicio in servicios_list:
            servicio.Fecha = servicio.Fecha.strftime("%d/%m/%Y")
            servicio.asistentes = Asistentes.objects.filter(servicio=servicio)
            for asistente in servicio.asistentes:
                factura = FacturasAsistentes.objects.filter(CodAsistente=asistente).first()
                asistente.factura = factura
        for  a in servicios_list:  
           print(a.asistentes)
     
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


@login_required(login_url='/accounts/login/')
def list_servicios(request):
    is_medico = False
    servicios_list = []

    if request.user.is_authenticated:
        if Medico.objects.filter(correo=request.user.email).exists():
            is_medico = True
            medico = Medico.objects.get(correo=request.user.email)
            servicios_list = servicios.objects.filter(codMedico=medico.codMedico)
            for servicio in servicios_list:
                servicio.Fecha = servicio.Fecha.strftime("%d/%m/%Y")

    formset = AsistentesFormSet(request.POST)
    form = serviciosForm(request.user, is_medico)

    context = {
        'segment': 'servicios',
        'servicios_list': servicios_list,
        'form': form,
        'formset': formset,
    }
    return render(request, 'medical_reports/servicios/list_servicios.html', context)



@login_required(login_url='/accounts/login/')
def create_servicio(request):
    if request.method == 'POST':
        form = serviciosForm(request.user,request.POST)
        formset = AsistentesFormSet(request.POST)
        factura_form = FacturasForm(request.POST)
        if form.is_valid() and formset.is_valid() and factura_form.is_valid():
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
            for asistente in asistentes_instances:
                factura_asistente = FacturasAsistentes(CodAsistente=asistente)
                factura_asistente.save()
            
            # Crear la factura si es pago a crédito
            if form.cleaned_data['MedioPago'] == 'Credito':
                factura = factura_form.save(commit=False)
                factura.CodProcedimiento = servicio
                factura.save()
                print("Si se salva el form de factura")
            
            return redirect('list_servicios')
    
    else:
        form = serviciosForm(request.user,initial={'EstadoPago': 'Pendiente'})
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
        form = serviciosForm(request.user,request.POST, instance=servicio)
        formset = AsistentesFormSet(request.POST, instance=servicio)
        
        if form.is_valid() and formset.is_valid():
            servicio = form.save(commit=False)
            if request.POST.get('NumeroFactura'):
                servicio.EstadoPago = 'Pagado'
            else:
                servicio.EstadoPago = 'Pendiente'
            servicio.save()
            formset.save()
            
            # Crear facturas para los asistentes
            asistentes_instances = formset.save(commit=False)
            for asistente in asistentes_instances:
                factura_asistente = FacturasAsistentes(CodAsistente=asistente)
                factura_asistente.save()
            
            if servicio.MedioPago == 'Credito':
                factura_form = FacturasForm(request.POST, instance=servicio.facturas_set.first())
                if factura_form.is_valid():
                    factura = factura_form.save(commit=False)
                    factura.CodProcedimiento = servicio
                    factura.estado = True
                    factura.save()
            
            if form.cleaned_data['MedioPago'] == 'Contado':
                if form.cleaned_data['numFactura'] != '0':
                    servicio.EstadoPago = 'Pagado' 
                else:
                    servicio.EstadoPago = 'Pendiente'
                servicio.save()

            return redirect('list_servicios')
    
    else:
        form = serviciosForm(request.user,instance=servicio)
        asistentes = servicio.asistentes_set.all()
        formset = AsistentesFormSet(instance=servicio, queryset=asistentes)
        
        # Filtrar las facturas de los asistentes asociados al servicio
        asistentes = formset.save(commit=False)
        facturas_asistentes = FacturasAsistentes.objects.filter(CodAsistente__in=asistentes)
        
        if servicio.MedioPago == 'Credito':
            factura_form = FacturasForm(instance=servicio.facturas_set.first())       

    context = {
        'segment': 'servicios',
        'form': form,
        'servicio': servicio,
        'formset': formset,
        'factura_form': factura_form,
        'is_update': True,
        "facturasis":facturas_asistentes,
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
            if form.cleaned_data['FechaEmision'] and form.cleaned_data['descFactura']:
                factura_asistente = form.save(commit=False)
                factura_asistente.CodAsistente = asistente
                factura_asistente.estado = True 
                factura_asistente.save()
                return redirect('update_servicio', pk=servicio.pk)
            else:
                messages.error(request, 'Para poder actualizar la factura es necesario que indique la fecha y número de factura ')
               
        else:
            print("No entro")
            print(form.errors)
    else:
        form = FacturasAsistentesForm(instance=factura_asistente)
    print(factura_asistente.estado)
    context = {
        'segment': 'Actualización de factura por asistente',
        'form': form,
        'servicio': servicio,
        'asistente': asistente,
        'factura_asistente':factura_asistente,
    }
    return render(request, 'medical_reports/servicios/update_factura.html', context)



# crear pagos......
@login_required(login_url='/accounts/login/')
def list_servicios_report(request):
    if Medico.objects.filter(correo=request.user.email).exists():
        medico = Medico.objects.get(correo=request.user.email)
        servicios_list = servicios.objects.filter(codMedico=medico.codMedico)
        for servicio in servicios_list:
            servicio.Fecha = servicio.Fecha.strftime("%d/%m/%Y")
            servicio.asistentes = Asistentes.objects.filter(servicio=servicio)
            for asistente in servicio.asistentes:
                factura = FacturasAsistentes.objects.filter(CodAsistente=asistente).first()
                asistente.factura = factura
        for  a in servicios_list:  
           print(a.asistentes)
     
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


#pagos
def procesar_pagos(request):
    if request.method == 'POST':
        start_date = request.POST.get('rango_fecha_inicio')
        end_date = request.POST.get('rango_fecha_fin')
        print("If 1")
        if start_date and end_date:
            print("If 2")
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")    
            if Medico.objects.filter(correo=request.user.email).exists():
                print("If 3")
                medico = Medico.objects.get(correo=request.user.email)
                servicios_list = servicios.objects.filter(
                    codMedico=medico.codMedico,
                    Fecha__range=(start_date, end_date),
                    EstadoCierre=False
                )   
                for servicio in servicios_list:
                    print("Servicio", servicio)
                    print("servicios_list", servicios_list)
                    print("for 1")
                    
                    # Debugging: Print values for debugging
                    print("servicio.CodProcedimiento:", servicio.CodProcedimiento)
                    print("servicio.CodProcedimiento.pk:", servicio)
                    factura_aseguradora = Facturas.objects.filter(
                        CodProcedimiento=servicio.CodProcedimiento, estado=True
                    ).first()
                    print("factura_aseguradora:", factura_aseguradora)
                    if factura_aseguradora or servicio.numFactura  != '0':
                        print("If 4")
                        servicio.asistentes = Asistentes.objects.filter(servicio=servicio)
                        asistentes_pagados = True                      
                        for asistente in servicio.asistentes:
                            print("for 2")
                            factura = FacturasAsistentes.objects.filter(
                                CodAsistente=asistente
                            ).first()
                            if factura is None or not factura.estado:
                                print("If 5")
                                asistentes_pagados = False
                                break                   
                        if asistentes_pagados:
                            print("If 6")
                            for asistente in servicio.asistentes:
                                print("for 3")
                                if not PagosAsistentes.objects.filter(
                                        CodOperacion=servicio,
                                        CodAsistente=asistente
                                ).exists():
                                    monto_asistente = asistente.CodCostoPorAsistente.MontoCosto
                                    pago = PagosAsistentes.objects.create(
                                        CodOperacion=servicio,
                                        CodAsistente=asistente,
                                        MontoPagado=monto_asistente,
                                        FechaPago=datetime.now()
                                    )
                                    factura.estado = True
                                    factura.save()
                                    
                            # Verificar si todas las facturas de asistentes tienen estado True
                            asistentes_todos_pagados = all(
                                FacturasAsistentes.object+s.filter(
                                    CodAsistente=asistente, estado=True
                                ).exists() for asistente in servicio.asistentes
                            )                         
                            if asistentes_todos_pagados:
                                print("If 7")
                                servicio.EstadoCierre = True
                                servicio.save()
                    else:
                       response_data = {'message': 'No hay factura o el if no sirvio'}
                response_data = {'message': 'Procesamiento de pagos completado'}
                return JsonResponse(response_data)
            else:
                pass
        else:
            response_data = {'error': 'Fechas de inicio y fin no proporcionadas'}
            return JsonResponse(response_data, status=400)
        context = {
        'segment': 'reportes',
        'response_data': response_data,
        'servicios_list':servicios_list,
    }
    return render(request, 'medical_reports/servicios/generarpagos.html', context)







