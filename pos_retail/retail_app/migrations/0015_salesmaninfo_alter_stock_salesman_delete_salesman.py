# Generated by Django 5.1 on 2025-01-13 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0014_rename_itemtype_item_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesmanInfo',
            fields=[
                ('salesman_id', models.AutoField(primary_key=True, serialize=False)),
                ('salesman_name', models.CharField(max_length=255)),
                ('salesman_contact', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salesmen', to='retail_app.companyinfo')),
            ],
        ),
        migrations.AlterField(
            model_name='stock',
            name='salesman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='retail_app.salesmaninfo'),
        ),
        migrations.DeleteModel(
            name='Salesman',
        ),
    ]
