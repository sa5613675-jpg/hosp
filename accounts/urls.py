from django.urls import path
from . import views
from . import pc_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pc-member/<str:pc_code>/commission/', views.manage_pc_commission, name='manage_pc_commission'),
    path('pc-rates/update/<str:member_type>/', views.update_default_rates, name='update_default_rates'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-finance/', views.admin_finance_dashboard, name='admin_finance'),
    path('admin-finance/add-expense/', views.quick_add_expense, name='quick_add_expense'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist-dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    
    # Reception Features - TODO: implement these views
    # path('reception/register-patient/', views.reception_register_patient, name='reception_register_patient'),
    # path('reception/billing/', views.reception_billing, name='reception_billing'),
    # path('reception/voucher/<int:appointment_id>/', views.reception_print_voucher, name='reception_print_voucher'),
    # path('reception/prescription/<int:prescription_id>/', views.reception_print_prescription, name='reception_print_prescription'),
    # path('reception/doctor-serials/<int:doctor_id>/', views.reception_doctor_serials, name='reception_doctor_serials'),
    
    path('lab-dashboard/', views.lab_dashboard, name='lab_dashboard'),
    path('pharmacy-dashboard/', views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('canteen-dashboard/', views.canteen_dashboard, name='canteen_dashboard'),
    
    # Lab Assistant Features
    path('lab-assistant/', views.lab_assistant_dashboard, name='lab_assistant_dashboard'),
    path('lab/create-bill/<int:appointment_id>/', views.create_lab_bill, name='create_lab_bill'),
    path('lab/bill/<int:bill_id>/voucher/', views.lab_bill_voucher, name='lab_bill_voucher'),
    path('lab/pending-bills/', views.pending_lab_bills, name='pending_lab_bills'),
    path('lab/collect-payment/<int:bill_id>/', views.collect_lab_payment, name='collect_lab_payment'),
    
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Reception Billing with PC Code & Discount
    path('reception/billing/lab/<int:order_id>/', views.reception_billing_lab, name='reception_billing_lab'),
    path('reception/billing/appointment/<int:appointment_id>/', views.reception_billing_appointment, name='reception_billing_appointment'),
    
    # Display Monitor
    path('display-monitor/', views.display_monitor, name='display_monitor'),
    
    # Dashboard Sub-Features
    path('user-management/', views.user_management, name='user_management'),
    path('doctor-management/', views.doctor_management, name='doctor_management'),
    path('update-doctor-fee/', views.update_doctor_fee, name='update_doctor_fee'),
    path('pharmacy-management/', views.pharmacy_management, name='pharmacy_management'),
    
    # Pharmacy Web Interface (User-friendly)
    path('add-medicine/', views.add_medicine, name='add_medicine'),
    path('view-medicines/', views.view_medicines, name='view_medicines'),
    path('edit-medicine/<int:medicine_id>/', views.edit_medicine, name='edit_medicine'),
    path('delete-medicine/<int:medicine_id>/', views.delete_medicine, name='delete_medicine'),
    path('add-stock/', views.add_stock, name='add_stock'),
    
    path('system-settings/', views.system_settings, name='system_settings'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('vitals/<int:appointment_id>/', views.patient_vitals_entry, name='patient_vitals_entry'),
    path('payment/<int:appointment_id>/', views.payment_collection, name='payment_collection'),
    
    # PC (Persistent Commission) System
    path('pc-dashboard/', pc_views.pc_dashboard, name='pc_dashboard'),
    path('pc-members/<str:member_type>/', pc_views.pc_member_list, name='pc_member_list'),
    path('pc-members/create/', pc_views.pc_member_create, name='pc_member_create'),
    path('pc-member/<str:pc_code>/', pc_views.pc_member_detail, name='pc_member_detail'),
    path('pc-member/<str:pc_code>/mark-paid/', pc_views.pc_mark_paid, name='pc_mark_paid'),
    path('pc-transaction/create/', pc_views.pc_transaction_create, name='pc_transaction_create'),
    
    # AJAX APIs
    path('api/pc-lookup/', pc_views.pc_lookup_api, name='pc_lookup_api'),
    path('api/call-next-patient/', views.call_next_patient, name='call_next_patient'),
    path('api/prescription/<int:prescription_id>/mark-printed/', views.mark_prescription_printed, name='mark_prescription_printed'),
]

