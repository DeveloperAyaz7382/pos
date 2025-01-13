# Generated by Django 5.1.4 on 2024-12-30 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0009_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('order_item_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('order_item_quantity', models.IntegerField()),
                ('order_item_unitprice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.inventory')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.order')),
            ],
        ),
    ]