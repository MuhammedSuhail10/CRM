# Generated by Django 4.2.5 on 2024-03-01 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('internship', models.CharField(max_length=100)),
                ('rate', models.CharField(max_length=100)),
                ('gst', models.CharField(max_length=100)),
                ('total_rate', models.CharField(max_length=100)),
                ('syllabus', models.FileField(upload_to='media/')),
            ],
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('won', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3)),
                ('created_on', models.DateField(auto_now=True)),
                ('delete_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='leeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('assign_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3)),
                ('lead_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Won', 'Won')], default='No', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='saleperson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=100)),
                ('todays_lead', models.IntegerField(default=0)),
                ('strength', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Won',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('Course', 'Course'), ('Internship', 'Internship')], max_length=100)),
                ('type', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline')], max_length=100)),
                ('won_on', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='crmAdmin.course')),
                ('duty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duty', to='crmAdmin.duty')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.IntegerField(default=0)),
                ('target_won', models.IntegerField(default=0)),
                ('target_remaining', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='crmAdmin.saleperson')),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(max_length=100)),
                ('screenshot', models.FileField(upload_to='media/')),
                ('won', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale', to='crmAdmin.won')),
            ],
        ),
        migrations.CreateModel(
            name='leadstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watsapp', models.CharField(max_length=100)),
                ('progress', models.CharField(choices=[('Not Contacted Yet', 'Not Contacted Yet'), ('Not Answering', 'Not Answering'), ('Busy', 'Busy'), ('Contacted', 'Contacted:Waiting For Reply'), ('Got Appointment', 'Got Appointment'), ('Payment', 'Payment'), ('Not Interested', 'Not Interested')], default='Not Contacted Yet', max_length=100)),
                ('status', models.CharField(choices=[('Not Answering', 'Not Answering'), ('Follow Up', 'Follow Up'), ('Won', 'Won'), ('Lost', 'Lost')], default='Not Answering', max_length=100)),
                ('last_contacted', models.DateField(auto_now=True)),
                ('probability', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('leed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crmAdmin.leeds')),
            ],
        ),
        migrations.AddField(
            model_name='duty',
            name='lead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lead', to='crmAdmin.leeds'),
        ),
        migrations.AddField(
            model_name='duty',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salesperson', to='crmAdmin.saleperson'),
        ),
        migrations.CreateModel(
            name='Daily_Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.IntegerField(default=0)),
                ('target_won', models.IntegerField(default=0)),
                ('target_remaining', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_sale', to='crmAdmin.saleperson')),
            ],
        ),
        migrations.CreateModel(
            name='callback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('duty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crmAdmin.duty')),
            ],
        ),
    ]