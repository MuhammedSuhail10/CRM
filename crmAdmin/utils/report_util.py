#################################  C S V  R E P O R T  G E N E R A T I O N  #################################
from io import StringIO
import csv,io,calendar
from django.core.files.base import ContentFile
from crmAdmin.models import *

def create_report(array, header, header_row, name):
    today = timezone.now().date()
    file_name = header
    with StringIO() as csv_buffer:
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(header_row)
        count = 0
        if name == "followup":
            for emp, status in array:
                csv_writer.writerow([count, emp, status.lead.name, status.lead.phone, status.progress, status.course, status.course.rate, status.notes])
                count +=1
        else:
            for won in array:
                csv_writer.writerow([count, won.employee, won.lead.name, won.lead.phone, won.course, won.course.rate, won.mode])
                count +=1
        csv_file = ContentFile(csv_buffer.getvalue().encode("utf-8"))
    follow_csv = Report.objects.create(name=name)
    follow_csv.csv.save(file_name, csv_file)