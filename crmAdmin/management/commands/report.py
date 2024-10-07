from django.core.management.base import BaseCommand
from crmAdmin.models import *
from django.utils import timezone
from datetime import timedelta, datetime
from crmAdmin.utils.report_util import *

class Command(BaseCommand):
    help = 'Update Daily'
    def handle(self, *args, **kwargs):
        self.followup()

        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(days=1) if start_of_month.month == 12 else start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(days=1)
        
        if today == end_of_month:
            self.monthly_follow(start_of_month, end_of_month)
            self.monthly_won(start_of_month, end_of_month)

    def followup(self):
        today = timezone.now().date()
        duty = Duty.objects.filter(lead__lead_status=True, lead__closed=False).order_by('-id')
        array = []
        for i in duty:
            if Leadstatus.objects.filter(lead=i.lead,contacted_on=today).exists():
                for leads in Leadstatus.objects.filter(lead=i.lead,contacted_on=today):
                    saleperson = i.emp.user.name if i.emp else "Not Asigned"
                    array.append((saleperson, leads))
        header = 'followups ' +today.strftime('%Y-%m-%d')+'.csv'
        header_row = [ '#', 'sale', 'lead', 'lead_number','progress', 'course', 'course_value', 'notes' ]
        create_report(array, header, header_row, "followup")

    def monthly_won(self, start_of_month, end_of_month):
        array = Won.objects.filter(won_on__gte=start_of_month,won_on__lte=end_of_month).order_by('-won_on')
        header_row = [ '#', 'sale', 'lead', 'lead_number', 'course', 'course_value', 'mode' ]
        header = 'monthly_won'+today.strftime('%m')+'.csv'
        create_report(array, header, header_row, "won")

    def monthly_follow(self, start_of_month, end_of_month):
        Report.objects.filter(name= 'followup').delete()
        duties = Duty.objects.filter(lead__lead_status=True, lead__closed=False, lead__trash=False).order_by('-id')
        array = []
        for i in duties:
            if Leadstatus.objects.filter(leed=i.lead,last_contacted__gte=start_of_month,last_contacted__lte=end_of_month).exists():
                for leads in Leadstatus.objects.filter(lead=i.lead,contacted_on=today):
                    saleperson = i.emp.user.name if i.emp else "Not Asigned"
                    array.append((saleperson, leads))
        header = 'monthly_followups ' +today.strftime('%Y-%m-%d')+'.csv'
        header_row = [ '#', 'sale', 'lead', 'lead_number','progress', 'course', 'course_value', 'notes' ]
        create_report(array, header, header_row, "followup")