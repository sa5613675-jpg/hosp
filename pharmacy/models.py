from django.db import models
from django.conf import settings
from patients.models import Patient
from appointments.models import Prescription

class DrugCategory(models.Model):
    """Medicine categories"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Drug Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Drug(models.Model):
    """Medicine/Drug inventory"""
    
    FORM_CHOICES = [
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('SYRUP', 'Syrup'),
        ('INJECTION', 'Injection'),
        ('CREAM', 'Cream/Ointment'),
        ('DROPS', 'Drops'),
        ('INHALER', 'Inhaler'),
        ('OTHER', 'Other'),
    ]
    
    drug_code = models.CharField(max_length=50, unique=True)
    generic_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200)
    category = models.ForeignKey(DrugCategory, on_delete=models.SET_NULL, null=True)
    
    # Form and strength
    form = models.CharField(max_length=20, choices=FORM_CHOICES)
    strength = models.CharField(max_length=50, help_text="e.g., 500mg, 10ml")
    
    # Manufacturer
    manufacturer = models.CharField(max_length=200)
    
    # Stock information
    quantity_in_stock = models.IntegerField(default=0)
    reorder_level = models.IntegerField(default=10, help_text="Alert when stock falls below this")
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Purchase/Buy price")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost price (for reference)")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Selling price to customer")
    
    # Dates
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    side_effects = models.TextField(blank=True)
    storage_instructions = models.CharField(max_length=200, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['brand_name']
        indexes = [
            models.Index(fields=['drug_code']),
            models.Index(fields=['generic_name']),
            models.Index(fields=['brand_name']),
        ]
    
    def __str__(self):
        return f"{self.brand_name} ({self.generic_name}) - {self.strength}"
    
    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level
    
    @property
    def is_expired(self):
        if not self.expiry_date:
            return False
        from django.utils import timezone
        return self.expiry_date < timezone.now().date()
    
    @property
    def days_until_expiry(self):
        if not self.expiry_date:
            return None
        from django.utils import timezone
        delta = self.expiry_date - timezone.now().date()
        return delta.days
    
    @property
    def profit_per_unit(self):
        """Profit per unit sold"""
        return self.selling_price - self.buy_price
    
    @property
    def profit_margin(self):
        """Profit margin percentage"""
        if self.buy_price > 0:
            return ((self.selling_price - self.buy_price) / self.buy_price) * 100
        return 0
    
    @property
    def stock_value_buy(self):
        """Total stock value at buy price"""
        return self.quantity_in_stock * self.buy_price
    
    @property
    def stock_value_sell(self):
        """Total stock value at selling price"""
        return self.quantity_in_stock * self.selling_price


class PharmacySale(models.Model):
    """Pharmacy sales transaction"""
    
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('MOBILE', 'Mobile Banking'),
        ('INSURANCE', 'Insurance'),
    ]
    
    sale_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Customer info (can be linked to patient or walk-in)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacy_purchases'
    )
    customer_name = models.CharField(max_length=200, blank=True, help_text="For walk-in customers")
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Prescription link (optional)
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pharmacy_sales'
    )
    
    # Sale details
    sale_date = models.DateTimeField(auto_now_add=True)
    served_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pharmacy_sales'
    )
    
    # Payment
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Total profit from this sale")
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='CASH')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change_returned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Auto-generated income
    income_created = models.BooleanField(default=False)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"{self.sale_number} - {self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.sale_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_sale = PharmacySale.objects.filter(
                sale_number__startswith=f'PH{date_str}'
            ).order_by('sale_number').last()
            
            if last_sale:
                last_number = int(last_sale.sale_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.sale_number = f'PH{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calculate sale totals"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.total_profit = sum(item.profit for item in self.items.all())
        self.total_amount = self.subtotal - self.discount + self.tax
        self.change_returned = self.amount_paid - self.total_amount if self.amount_paid > self.total_amount else 0
        self.save()
        
        # Create income if not already created
        if not self.income_created:
            self.create_income()
    
    def create_income(self):
        """Auto-create income in finance app"""
        from finance.models import Income
        
        try:
            income = Income.objects.create(
                source='PHARMACY',
                amount=self.total_amount,
                date=self.sale_date.date(),
                description=f"Pharmacy Sale: {self.sale_number}",
                reference_number=self.sale_number,
                payment_method=self.payment_method,
                recorded_by=self.served_by
            )
            self.income_created = True
            self.save()
            return income
        except Exception as e:
            print(f"Error creating income: {e}")
            return None


class SaleItem(models.Model):
    """Individual items in a pharmacy sale"""
    
    sale = models.ForeignKey(PharmacySale, on_delete=models.CASCADE, related_name='items')
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
    
    quantity = models.IntegerField(default=1)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Buy price for profit calculation")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Profit from this item")
    
    batch_number = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.drug.brand_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        self.buy_price = self.drug.buy_price
        self.profit = (self.unit_price - self.buy_price) * self.quantity
        
        super().save(*args, **kwargs)
        
        # Update drug stock
        if self.pk is None:  # New item only
            self.drug.quantity_in_stock -= self.quantity
            self.drug.save()


class StockAdjustment(models.Model):
    """Track stock adjustments (purchases, returns, expired, etc.)"""
    
    ADJUSTMENT_TYPE_CHOICES = [
        ('PURCHASE', 'Purchase'),
        ('RETURN', 'Return to Supplier'),
        ('EXPIRED', 'Expired'),
        ('DAMAGED', 'Damaged'),
        ('CORRECTION', 'Stock Correction'),
    ]
    
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='adjustments')
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPE_CHOICES)
    
    quantity = models.IntegerField(help_text="Positive for additions, negative for removals")
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    reason = models.TextField()
    adjusted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    adjusted_at = models.DateTimeField(auto_now_add=True)
    
    # Purchase info
    supplier = models.CharField(max_length=200, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    
    # Auto-generated expense
    expense_created = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-adjusted_at']
    
    def __str__(self):
        return f"{self.drug.brand_name} - {self.adjustment_type} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Update drug stock
        self.drug.quantity_in_stock += self.quantity
        self.drug.save()
        
        # Create expense for purchases
        if is_new and self.adjustment_type == 'PURCHASE' and not self.expense_created:
            self.create_expense()
    
    def create_expense(self):
        """Auto-create expense when medicine is purchased"""
        from finance.models import Expense
        
        try:
            total_cost = abs(self.quantity) * self.unit_cost
            expense = Expense.objects.create(
                expense_type='SUPPLIES',
                amount=total_cost,
                date=self.adjusted_at.date(),
                description=f"Medicine Purchase: {self.drug.brand_name} - {self.quantity} units",
                vendor=self.supplier if self.supplier else 'Pharmacy Supplier',
                invoice_number=self.invoice_number,
                recorded_by=self.adjusted_by,
                is_approved=True
            )
            self.expense_created = True
            self.save()
            return expense
        except Exception as e:
            print(f"Error creating expense: {e}")
            return None
