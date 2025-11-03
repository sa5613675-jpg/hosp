from django.contrib import admin
from .models import LabTest, LabOrder, LabResult, LabBill


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    """Admin for Lab Tests - add test names and prices"""
    
    list_display = ['test_code', 'test_name', 'category', 'price', 'turnaround_time', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['test_code', 'test_name', 'description']
    list_editable = ['price', 'is_active']
    
    fieldsets = (
        ('Test Information', {
            'fields': ('test_code', 'test_name', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price',)
        }),
        ('Sample Requirements', {
            'fields': ('sample_type', 'sample_volume', 'preparation_instructions')
        }),
        ('Processing', {
            'fields': ('turnaround_time', 'is_active')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing
            return ['test_code']
        return []


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    """Admin for Lab Orders"""
    
    list_display = ['order_number', 'patient', 'ordered_by', 'status', 'total_amount', 'is_paid', 'ordered_at']
    list_filter = ['status', 'is_paid', 'priority', 'ordered_at']
    search_fields = ['order_number', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['order_number', 'total_amount', 'ordered_at']
    filter_horizontal = ['tests']
    date_hierarchy = 'ordered_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'patient', 'appointment')
        }),
        ('Tests', {
            'fields': ('tests', 'clinical_notes', 'priority')
        }),
        ('Status', {
            'fields': ('status', 'ordered_by', 'ordered_at')
        }),
        ('Sample Collection', {
            'fields': ('sample_collected_at', 'sample_collected_by')
        }),
        ('Billing', {
            'fields': ('total_amount', 'is_paid')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new
            obj.ordered_by = request.user
        super().save_model(request, obj, form, change)
        
        # Calculate total after saving
        if obj.pk:
            obj.calculate_total()


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    """Admin for Lab Results"""
    
    list_display = ['order', 'test', 'is_verified', 'tested_by', 'tested_at']
    list_filter = ['is_verified', 'tested_at', 'is_printed']
    search_fields = ['order__order_number', 'test__test_name']
    readonly_fields = ['tested_at', 'verified_at']
    
    fieldsets = (
        ('Result Information', {
            'fields': ('order', 'test')
        }),
        ('Results', {
            'fields': ('result_data', 'interpretation', 'notes')
        }),
        ('Testing', {
            'fields': ('tested_by', 'tested_at')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_by', 'verified_at')
        }),
        ('Report', {
            'fields': ('report_file', 'is_printed')
        }),
    )


@admin.register(LabBill)
class LabBillAdmin(admin.ModelAdmin):
    """Admin for Lab Bills"""
    
    list_display = ['bill_number', 'patient', 'payment_status', 'total_amount', 'created_by', 'created_at']
    list_filter = ['payment_status', 'created_at', 'collected_at']
    search_fields = ['bill_number', 'patient__name', 'patient__phone']
    readonly_fields = ['bill_number', 'subtotal', 'total_amount', 'created_at', 'collected_at', 'income_created']
    filter_horizontal = ['tests']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('bill_number', 'patient', 'appointment')
        }),
        ('Tests & Pricing', {
            'fields': ('tests', 'subtotal', 'discount', 'total_amount')
        }),
        ('Payment', {
            'fields': ('payment_status', 'payment_method', 'paid_amount')
        }),
        ('Staff', {
            'fields': ('created_by', 'created_at', 'collected_by', 'collected_at', 'income_created')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
        # Calculate total after saving
        if obj.pk and 'tests' in form.changed_data:
            obj.calculate_total()

