from django.contrib import admin
from .models_commission import PCCommissionRate

@admin.register(PCCommissionRate)
class PCCommissionRateAdmin(admin.ModelAdmin):
    """Admin interface for PC Commission Rates"""
    
    list_display = ['member_type', 'test_type', 'commission_percentage']
    list_filter = ['member_type', 'test_type']
    search_fields = ['member_type', 'test_type']
    
    fieldsets = (
        (None, {
            'fields': ('member_type', 'test_type', 'commission_percentage')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of commission rates"""
        return False  # Rates should be updated, not deleted