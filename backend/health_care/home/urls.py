from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import tables

urlpatterns = [
  path(''       , views.index, name='index'),
  path('tables/', tables     , name='tables'),

  # Components
  path('components/button/', views.bc_button, name='bc_button'),
  path('components/badges/', views.bc_badges, name='bc_badges'),
  path('components/breadcrumb-pagination/', views.bc_breadcrumb_pagination, name='bc_breadcrumb_pagination'),
  path('components/collapse/', views.bc_collapse, name='bc_collapse'),
  path('components/tabs/', views.bc_tabs, name='bc_tabs'),
  path('components/typography/', views.bc_typography, name='bc_typography'),
  path('components/feather-icon/', views.icon_feather, name='icon_feather'),

  # Forms and Tables
  path('forms/form-elements/', views.form_elements, name='form_elements'),
  path('tables/basic-tables/', views.basic_tables, name='basic_tables'),

  # Chart and Maps
  path('charts/morris-chart/', views.morris_chart, name='morris_chart'),
  path('maps/google-maps/', views.google_maps, name='google_maps'),

  # Authentication
  path('accounts/register/', views.UserRegistrationView.as_view(), name='register'),
  path('accounts/login/', views.UserLoginView.as_view(), name='login'),
  path('accounts/logout/', views.logout_view, name='logout'),

  path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
  path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
      template_name='accounts/auth-password-change-done.html'
  ), name="password_change_done"),

  path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
  path('accounts/password-reset-confirm/<uidb64>/<token>/',
    views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
  ),
  path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
    template_name='accounts/auth-password-reset-done.html'
  ), name='password_reset_done'),
  path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
    template_name='accounts/auth-password-reset-complete.html'
  ), name='password_reset_complete'),

  #
  path('profile/', views.profile, name='profile'),
  path('sample-page/', views.sample_page, name='sample_page'),
  path('services/', views.profile, name='services'),
  # Medico
  path('medico/', views.medico_list, name='medico_list'),
  path('medico/create/', views.medico_create, name='medico_create'),
  path('medico/<int:codMedico>/', views.medico_detail, name='medico_detail'),
  path('medico/<int:codMedico>/update/', views.medico_update, name='medico_update'),
  path('medico/<int:codMedico>/delete/', views.medico_delete, name='medico_delete'),
  #Aseguradoras
  path('agregar/aseguradora/', views.create_insurer, name='agregar_aseguradora'),
  path('listar/aseguradoras/', views.list_insurers, name='listar_aseguradoras'),
  path('actualizar/<int:pk>/', views.update_insurer, name='actualizar_aseguradora'),
  path('eliminar_aseguradora/<int:pk>/', views.eliminar_aseguradora, name='eliminar_aseguradora'),
  
  #Emisores
  path('listar/emisores/', views.list_emitters, name='list_emisores'),
  path('agregar/emisores/', views.emitters, name='create_emisores'),
  path('actualizar/<int:pk>/', views.update_insurer, name='actualizar_emisor'),
  path('eliminar/emisores/<int:pk>/', views.eliminar_aseguradora, name='eliminar_emisor'),
  path('get_emisor/<int:pk>/', views.get_emisor, name='get_emisor'),
  
  #Pagos Asistente
  path('pagos_asistentes/', views.list_costos, name='pagos_asistentes'),
  path('crear_pago/', views.costos_por_asistente, name='crear_pago'),
  path('actualizar_pago/<int:pk>/', views.update_costo, name='actualizar_pago'),
  path('eliminar_pago/<int:pk>/', views.eliminar_costo, name='eliminar_pago'),
  
  #Costo de servicios
  path('costos_servicios/', views.list_servicio, name='list_servicio'),
  path('crear_servicio/', views.costos_por_servicio, name='costos_por_servicio'),
  path('actualizar/<int:pk>/', views.update_costo, name='update_costo'),
  path('eliminar/<int:pk>/', views.eliminar_costo, name='eliminar_costo'),
  
  #asistentes
  path('asistentes/', views.list_asistentes, name='asistentes_list'),
  path('asistentes/create/', views.create_asistente, name='asistente_create'),
  path('asistentes/<int:pk>/update/', views.update_asistente, name='asistente_update'),
  path('asistentes/<int:pk>/delete/', views.delete_asistente, name='asistente_delete'),
  
  #Servicios
  path('servicios/', views.list_servicios, name='list_servicios'),
  path('servicios/create/', views.create_servicio, name='create_servicio'),
  path('servicios/<int:pk>/update/', views.update_servicio, name='update_servicio'),
  path('servicios/<int:pk>/delete/', views.delete_servicio, name='delete_servicio'),
  path('obtener_monto_costo/<int:cod_costo_operacion_id>/', views.obtener_monto_costo, name='obtener_monto_costo'),
]

