# Generated by Django 4.2.5 on 2024-05-10 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmAdmin', '0003_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total', models.IntegerField()),
                ('follow', models.IntegerField()),
                ('Notanswer', models.IntegerField()),
                ('Notinterested', models.IntegerField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='crmAdmin.saleperson')),
            ],
        ),
    ]