from django.core.management.base import BaseCommand
from crmAdmin.models import *
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
class Command(BaseCommand):
    help = 'Update Daily'
    def handle(self, *args, **kwargs):
        yesterday = timezone.now().date() - timedelta(days=1)
        today = datetime.now().date()
        for i in saleperson.objects.all():
            i.todays_lead = 0
            i.save()
        for i in Daily_Target.objects.all():
            i.target_won = 0
            i.target_remaining = int(i.target)
            i.save()
        for i in Duty.objects.all():
            if today == i.delete_date and (i.lead.lead_status == 'No' or i.lead.lead_status == 'NA'):
                lead = leeds.objects.get(number=i.lead.number)
                lead.assign_status = 'No'
                lead.save()
                i.delete()