# Generated by Django 4.2.5 on 2024-10-04 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0003_lead_trash'),
    ]

    operations = [
        migrations.AddField(
            model_name='won',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crmAdmin.employee'),
        ),
    ]
