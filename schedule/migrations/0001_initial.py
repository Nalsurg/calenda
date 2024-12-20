# Generated by Django 4.2.11 on 2024-11-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Event Title')),
                ('start', models.DateTimeField(verbose_name='Start Time')),
                ('end', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Event Description')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ['start'],
            },
        ),
    ]
