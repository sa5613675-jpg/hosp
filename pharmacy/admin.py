from django.contrib import admin
from .models import DrugCategory, Drug, PharmacySale, SaleItem, StockAdjustment


@admin.register(DrugCategory)
class DrugCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['drug_code', 'brand_name', 'generic_name', 'form', 'strength', 
                    'quantity_in_stock', 'buy_price', 'selling_price', 'manufacturer']
    list_filter = ['form', 'category', 'manufacturer']
    search_fields = ['drug_code', 'brand_name', 'generic_name']
    list_editable = ['quantity_in_stock', 'buy_price', 'selling_price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('drug_code', 'generic_name', 'brand_name', 'category')
        }),
        ('Form and Dosage', {
            'fields': ('form', 'strength', 'manufacturer')
        }),
        ('Pricing', {
            'fields': ('buy_price', 'unit_price', 'selling_price')
        }),
        ('Stock', {
            'fields': ('quantity_in_stock', 'reorder_level')
        }),
        ('Additional Info', {
            'fields': ('description', 'expiry_date', 'batch_number'),
            'classes': ('collapse',)
        }),
    )


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['drug', 'quantity', 'unit_price', 'total_price', 'buy_price', 'profit']
    readonly_fields = ['total_price', 'profit']


@admin.register(PharmacySale)
class PharmacySaleAdmin(admin.ModelAdmin):
    list_display = ['sale_number', 'sale_date', 'patient', 'prescription', 
                    'total_amount', 'total_profit', 'payment_method', 'served_by']
    list_filter = ['payment_method', 'sale_date', 'served_by']
    search_fields = ['sale_number', 'patient__name', 'prescription__prescription_number', 
                     'customer_name', 'customer_phone']
    readonly_fields = ['sale_number', 'total_amount', 'total_profit', 'income_created', 'change_returned']
    inlines = [SaleItemInline]
    
    fieldsets = (
        ('Sale Information', {
            'fields': ('sale_number', 'sale_date', 'patient', 'prescription')
        }),
        ('Walk-in Customer (Optional)', {
            'fields': ('customer_name', 'customer_phone'),
            'classes': ('collapse',)
        }),
        ('Payment', {
            'fields': ('subtotal', 'discount', 'tax', 'total_amount', 'payment_method', 
                      'amount_paid', 'change_returned', 'total_profit')
        }),
        ('Staff & Notes', {
            'fields': ('served_by', 'notes', 'income_created')
        }),
    )


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'drug', 'quantity', 'unit_price', 'total_price', 
                    'buy_price', 'profit']
    list_filter = ['sale__sale_date']
    search_fields = ['drug__brand_name', 'sale__sale_number']
    readonly_fields = ['total_price', 'profit']


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ['drug', 'adjustment_type', 'quantity', 'unit_cost', 'reason', 
                    'adjusted_by', 'adjusted_at']
    list_filter = ['adjustment_type', 'adjusted_at', 'adjusted_by']
    search_fields = ['drug__brand_name', 'reason', 'supplier', 'invoice_number']
    readonly_fields = ['expense_created', 'adjusted_at']
    
    fieldsets = (
        ('Adjustment Details', {
            'fields': ('drug', 'adjustment_type', 'quantity', 'unit_cost', 'reason')
        }),
        ('Purchase Info', {
            'fields': ('supplier', 'invoice_number', 'batch_number'),
            'classes': ('collapse',)
        }),
        ('Staff & Date', {
            'fields': ('adjusted_by', 'adjusted_at', 'expense_created')
        }),
    )
