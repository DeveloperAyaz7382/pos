# Generated by Django 5.1.4 on 2024-12-25 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(max_length=20, unique=True)),
                ('type_name', models.CharField(max_length=100)),
                ('type_description', models.TextField()),
            ],
        ),
    ]
