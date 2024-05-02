from django.core.management.base import BaseCommand
from crmAdmin.models import *
from django.utils import timezone
from io import StringIO
import csv,io,calendar
from django.core.files.base import ContentFile
from datetime import timedelta, datetime
class Command(BaseCommand):
    help = 'Update Daily'
    def handle(self, *args, **kwargs):
        self.followup()
        self.monthly_rep()

    def followup(self):
        today = timezone.now().date()
        duty = Duty.objects.filter(lead__lead_status='Yes').order_by('-created_on')
        list = []
        for i in duty:
            leads = leadstatus.objects.filter(leed=i.lead,last_contacted=today).last()
            if leads:
                dut = Duty.objects.get(lead=i.lead)
                if dut.sale:
                    saleperson = dut.sale.user.first_name
                    list.append((saleperson, leads))
                else:
                    list.append(('Not Asigned', leads))
        header_row = [
            '#', 'sale', 'lead', 'lead_number','progress', 'course', 'course_value', 'notes'
        ]
        file_name = 'followups '+today.strftime('%Y-%m-%d')+'.csv'
        with StringIO() as csv_buffer:
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(header_row)
            f=1
            for j,i in list:
                c = course.objects.filter(name=i.course).exists()
                if c:
                    courses = course.objects.get(name=i.course)
                    value = courses.rate
                csv_writer.writerow([f,j,i.leed.name,i.leed.number,i.progress,i.course,value,i.notes])
                f +=1
            csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8"))
        follow_csv = Report.objects.create(name='followup')
        follow_csv.csv.save(file_name,csv_file)

    def monthly_rep(self):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        if start_of_month.month == 12:
            end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(days=1)
        if today == end_of_month:
            won = Won.objects.filter(won_on__gte=start_of_month,won_on__lte=end_of_month).order_by('-won_on')
            header_row = [
                '#', 'sale', 'lead', 'lead_number', 'course', 'course_value', 'mode'
            ]
            file_name = 'monthlywon'+today.strftime('%m')+'.csv'
            with StringIO() as csv_buffer:
                csv_writer = csv.writer(csv_buffer)
                csv_writer.writerow(header_row)
                f=1
                for i in won:
                    c = course.objects.filter(name=i.course).exists()
                    if c:
                        courses = course.objects.get(name=i.course)
                        value = courses.rate
                    csv_writer.writerow([f,i.duty.sale,i.duty.lead.name,i.duty.lead.number,i.course,value,i.mode])
                    f +=1
                csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8"))
            won_csv = Report.objects.create(name='monthlywon')
            won_csv.csv.save(file_name,csv_file)
            duty = Duty.objects.filter(lead__lead_status='Yes').order_by('-created_on')
            list = []
            for i in duty:
                leads = leadstatus.objects.filter(leed=i.lead).last()
                if leads:
                    dut = Duty.objects.get(lead=i.lead,created_on__gte=start_of_month,created_on__lte=end_of_month,)
                    if dut.sale:
                        saleperson = dut.sale.user.first_name
                        list.append((saleperson, leads))
                    else:
                        list.append(('Not Asigned', leads))
            header_row = [
                '#', 'sale', 'lead', 'lead_number','progress', 'course', 'course_value', 'notes','date'
            ]
            file_name = 'monthlyfollowups'+today.strftime('%m')+'.csv'
            with StringIO() as csv_buffer:
                csv_writer = csv.writer(csv_buffer)
                csv_writer.writerow(header_row)
                f=1
                for j,i in list:
                    if i.course:
                        c = course.objects.filter(name=i.course).exists()
                        if c:
                            courses = course.objects.get(name=i.course)
                            value = courses.rate
                        else:
                            value = 0
                        csv_writer.writerow([f,j,i.leed.name,i.leed.number,i.progress,i.course,value,i.notes,i.last_contacted])
                    f +=1
                csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8"))
            follow_csv = Report.objects.create(name='monthlyfollowup')
            follow_csv.csv.save(file_name,csv_file)
            for i in Report.objects.filter(name= 'followup'):
                i.delete()