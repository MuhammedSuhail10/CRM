# Generated by Django 4.2.5 on 2024-05-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0005_alter_salereport_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleperson',
            name='total_lead',
            field=models.IntegerField(default=0),
        ),
    ]