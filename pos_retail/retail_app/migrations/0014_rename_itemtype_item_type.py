# Generated by Django 5.1 on 2025-01-12 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retail_app', '0013_alter_wastage_wastage_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ItemType',
            new_name='Item_Type',
        ),
    ]
