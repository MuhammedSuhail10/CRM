# Generated by Django 4.2.5 on 2025-02-18 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='campain_leads',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lead',
            name='created_on',
            field=models.DateField(auto_now=True),
        ),
    ]
