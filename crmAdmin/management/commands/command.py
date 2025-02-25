from django.core.management.base import BaseCommand
from crmAdmin.models import *
from django.utils import timezone
from datetime import timedelta, datetime
import calendar

class Command(BaseCommand):
    help = 'Update Daily'
    def handle(self, *args, **kwargs):
        today = datetime.now().date()
        start_of_month = today.replace(day=1)
        yesterday = timezone.now().date() - timedelta(days=1)

        self.reset_employee()
        self.reset_target()
        self.delete_duty(yesterday)
        self.create_sale_report()

        if today == start_of_month:
            self.reset_monthly_target()

    def remove_leads(self):
        for i in Lead.objects.all():
            if Lead.objects.filter(phone=i.phone).count() > 1:
                duplicate_leads = Lead.objects.filter(phone=i.phone)
                duplicate_leads.exclude(id=i.id).delete()
            if i.phone.startswith("+91") or i.phone.startswith("91") and len(i.phone) > 10:
                i.phone = i.phone[3:] if i.phone.startswith("+91") else i.phone[2:]
                i.save()

    def reset_employee(self):
        for i in Employee.objects.all():
            i.todays_lead = 0
            i.save()

    def reset_target(self):
        for i in Target.objects.filter(type="Daily"):
            i.target_won = 0
            i.target_remaining = i.target
            i.save()

    def reset_monthly_target(self):
        target = Target.objects.filter(type="Monthly").last()
        new_monthly = Target.objects.create(target=target.target, target_won=0, target_remaining=target.target)
        new_monthly.save()

    def delete_duty(self, yesterday):
        for i in Duty.objects.all():
            if yesterday == i.delete_date and (i.lead.lead_status == False and i.lead.closed == False):
                lead = Lead.objects.get(id=i.lead.id)
                lead.assign_status = False
                lead.save()
                i.delete()

    def create_sale_report(self):
        for i in Employee.objects.all():
            report = SaleReport.objects.create(emp=i)