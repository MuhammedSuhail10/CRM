# Generated by Django 4.2.5 on 2024-03-27 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadstatus',
            name='course',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]