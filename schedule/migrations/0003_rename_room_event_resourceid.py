# Generated by Django 4.2.11 on 2024-11-26 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_event_room'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='room',
            new_name='resourceId',
        ),
    ]
