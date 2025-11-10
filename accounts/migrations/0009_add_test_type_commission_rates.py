from django.db import migrations, models
from decimal import Decimal

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pcmember',
            name='normal_test_commission',
            field=models.DecimalField(
                max_digits=5,
                decimal_places=2,
                default=Decimal('15.00'),
                help_text='Commission percentage for normal tests'
            ),
        ),
        migrations.AddField(
            model_name='pcmember',
            name='digital_test_commission',
            field=models.DecimalField(
                max_digits=5,
                decimal_places=2,
                default=Decimal('20.00'),
                help_text='Commission percentage for digital tests'
            ),
        ),
        migrations.AlterField(
            model_name='pcmember',
            name='commission_percentage',
            field=models.DecimalField(
                max_digits=5,
                decimal_places=2,
                default=Decimal('15.00'),
                help_text='Default commission percentage (for non-test services)'
            ),
        ),
    ]