from django.db.models.signals import *
from django.dispatch import receiver
from .models import *
from datetime import datetime

# Update Employers Details when Employee (Model) is deleted
@receiver(pre_delete, sender=Employee)
def before_delete_handler(sender, instance, **kwargs):
    if Duty.objects.filter(emp=instance).exists():
        duty = Duty.objects.get(emp=instance)
        duty.delete()

# Update Employers Details and Lead Details when Duty (Model) is deleted
@receiver(pre_delete, sender=Duty)
def before_delete_handler(sender, instance, **kwargs):
    emp = instance.emp
    if instance.created_on == datetime.now().date():
        emp.todays_lead -= 1
    emp.total_lead -= 1
    if emp.todays_lead > emp.total_lead:
        emp.total_lead = emp.todays_lead
    emp.save()
    leads = instance.lead
    leads.assign_status = False
    leads.save()