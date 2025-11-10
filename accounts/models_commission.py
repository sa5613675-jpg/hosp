from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PCCommissionRate(models.Model):
    """Commission rates for different PC member types and test types"""
    
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
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Commission percentage (e.g., 30 for 30%)"
    )
    
    class Meta:
        unique_together = ['member_type', 'test_type']
        verbose_name = "PC Commission Rate"
        verbose_name_plural = "PC Commission Rates"
    
    def __str__(self):
        return f"{self.member_type} - {self.test_type}: {self.commission_percentage}%"