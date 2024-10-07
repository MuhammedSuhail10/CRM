from django.db.models.signals import *
from django.dispatch import receiver
from crmAdmin.models import *
from datetime import datetime

# Update when a lead status is created
@receiver(post_save, sender=Leadstatus)
def log_model_save(sender, instance, created, **kwargs):
    if created:
        lead = instance.lead
        duty = Duty.objects.get(lead=lead)
        if instance.status == 'Follow Up' or instance.status == 'Won':
            lead.lead_status = True
            lead.save()
            if Target.objects.filter(sale=duty.emp, date=datetime.now(), type="Daily").exists():
                daily = Target.objects.get(sale=duty.emp, date=datetime.now(), type="Daily")
                daily.target_won += 1
                daily.target_remaining -= 1
                daily.save()
        elif instance.status == 'Won':
            lead.closed = True
            lead.save()
        elif instance.status == 'Lost':
            lead.trash = True
            lead.save()
            trash = TrashLead.objects.create(lead=lead,lost=True)
            trash.save()

        lead_statuses = Leadstatus.objects.filter(lead=lead)[:3]
        all_false = len(lead_statuses) > 0 and all(status.status == "Not Answering" for status in lead_statuses)
        print(f'The status of last 3 is {all_false}')
        if all_false:
            lead.trash =True
            lead.save()
            trash = TrashLead.objects.create(lead=lead,lost=False)
            trash.save()

@receiver(post_save, sender=Won)
def log_model_save(sender, instance, created, **kwargs):
    if created:
        duty = Duty.objects.get(lead=instance.lead)
        duty.delete()
        lead = instance.lead
        lead.closed = True
        lead.save()
        daily = Target.objects.get(sale=instance.employee, date__month=datetime.now().month, type="Monthly")
        daily.target_won += instance.course.rate
        daily.target_remaining -= instance.course.rate
        daily.save()