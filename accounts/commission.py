from django.db import models
from django.contrib import admin

class PCCommissionRate(models.Model):
    MEMBER_TYPE_CHOICES = [
        ('GENERAL', 'General Member'),
        ('LIFETIME', 'Lifetime Member'),
        ('INVESTOR', 'Investor Member'),
    ]
    
    TEST_TYPE_CHOICES = [
        ('NORMAL', 'Normal Test'),
        ('DIGITAL', 'Digital Test'),
    ]
    
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES)
    test_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Commission percentage (e.g., 30 for 30%)"
    )
    
    class Meta:
        unique_together = ['member_type', 'test_type']
        verbose_name = "PC Commission Rate"
        verbose_name_plural = "PC Commission Rates"
    
    def __str__(self):
        return f"{self.get_member_type_display()} - {self.get_test_type_display()}: {self.commission_percentage}%"

@admin.register(PCCommissionRate)
class PCCommissionRateAdmin(admin.ModelAdmin):
    list_display = ['member_type', 'test_type', 'commission_percentage']
    list_filter = ['member_type', 'test_type']
    search_fields = ['member_type', 'test_type']