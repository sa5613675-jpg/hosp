from django.db import migrations
from decimal import Decimal

def set_default_commission_rates(apps, schema_editor):
    PCMember = apps.get_model('accounts', 'PCMember')
    
    # Update commission rates based on member type
    PCMember.objects.filter(member_type='GENERAL').update(
        commission_percentage=Decimal('15.00'),
        normal_test_commission=Decimal('15.00'),
        digital_test_commission=Decimal('20.00')
    )
    
    PCMember.objects.filter(member_type='LIFETIME').update(
        commission_percentage=Decimal('20.00'),
        normal_test_commission=Decimal('20.00'),
        digital_test_commission=Decimal('25.00')
    )
    
    PCMember.objects.filter(member_type='PREMIUM').update(
        commission_percentage=Decimal('25.00'),
        normal_test_commission=Decimal('25.00'),
        digital_test_commission=Decimal('30.00')
    )

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_add_test_type_commission_rates'),
    ]

    operations = [
        migrations.RunPython(set_default_commission_rates),
    ]