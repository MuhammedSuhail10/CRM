# Generated by Django 4.2.5 on 2024-10-04 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]