# Generated by Django 3.1.7 on 2021-03-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vanity_app', '0002_service_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='booked_users',
            field=models.ManyToManyField(related_name='appointments', to='vanity_app.User'),
        ),
    ]
