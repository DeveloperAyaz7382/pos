# Generated by Django 5.1.4 on 2024-12-30 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0008_stockexpiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order_customer_name', models.CharField(max_length=255)),
                ('order_date', models.DateTimeField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_payment_status', models.CharField(max_length=50)),
                ('order_status', models.CharField(max_length=50)),
                ('order_remarks', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
