# Generated by Django 5.1.4 on 2024-12-26 09:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0004_salesman'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('item_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=255)),
                ('item_status', models.IntegerField(choices=[(1, 'Active'), (0, 'Inactive')], default=1)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.companyinfo')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.itemtype')),
            ],
        ),
    ]
