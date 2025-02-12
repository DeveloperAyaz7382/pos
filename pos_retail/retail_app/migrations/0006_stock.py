# Generated by Django 5.1.4 on 2024-12-30 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0005_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stock_quantity', models.IntegerField()),
                ('stock_unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_total_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('stock_entry_date', models.DateField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.inventory')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.salesman')),
            ],
        ),
    ]
