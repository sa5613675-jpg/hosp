from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Public URLs (no login required) - MUST BE FIRST
    path('book/', views.public_booking, name='public_booking'),
    path('online-booking/', views.online_booking, name='online_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('monitor/', views.display_monitor, name='display_monitor'),
    path('tts/bengali/', views.bengali_tts, name='bengali_tts'),
    
    # Staff-only URLs (login required)
    path('create/', views.appointment_create, name='appointment_create'),
    path('queue/', views.queue_display, name='queue_display'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/call/', views.call_patient, name='call_patient'),
    path('<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
    
    # Prescriptions
    path('<int:appointment_id>/prescription/create/', views.prescription_create, name='prescription_create'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescription/<int:pk>/print/', views.prescription_print, name='prescription_print'),
    
    # Doctor's appointment list by date
    path('my-appointments/', views.doctor_appointments_by_date, name='doctor_appointments_by_date'),
    
    # Reception prescriptions list
    path('prescriptions/reception/', views.reception_prescriptions_list, name='reception_prescriptions_list'),
    
    # List view - MUST BE LAST (catches everything else)
    path('', views.appointment_list, name='appointment_list'),
]
