# Generated by Django 4.2.11 on 2024-11-28 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_rename_resourceid_event_resource_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='resource_id',
            new_name='resourceId',
        ),
    ]
