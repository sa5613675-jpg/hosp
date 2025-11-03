# Generated migration for pharmacy management enhancements

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0001_initial'),  # Adjust based on your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Purchase/Buy price', max_digits=10),
        ),
        migrations.AddField(
            model_name='pharmacysale',
            name='total_profit',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total profit from this sale', max_digits=10),
        ),
        migrations.AddField(
            model_name='pharmacysale',
            name='income_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='buy_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Buy price for profit calculation', max_digits=10),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Profit from this item', max_digits=10),
        ),
        migrations.AddField(
            model_name='stockadjustment',
            name='expense_created',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='drug',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, help_text='Cost price (for reference)', max_digits=10),
        ),
        migrations.AlterField(
            model_name='drug',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, help_text='Selling price to customer', max_digits=10),
        ),
    ]
