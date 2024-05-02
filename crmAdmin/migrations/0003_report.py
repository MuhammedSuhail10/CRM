# Generated by Django 4.2.5 on 2024-05-02 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0002_leadstatus_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('csv', models.FileField(upload_to='report')),
                ('created_on', models.DateField(auto_now=True)),
            ],
        ),
    ]