from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class leeds(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    assign_status = models.CharField(max_length=3,choices=[('Yes', 'Yes'), ('No', 'No')],default='No')
    lead_status = models.CharField(max_length=3,choices=[('Yes', 'Yes'), ('No', 'No'),('Won', 'Won')],default='No')
    def __str__(self):
        return self.name
class leadstatus(models.Model):
    leed=models.ForeignKey(leeds,on_delete=models.CASCADE)
    watsapp = models.CharField(max_length=100)
    progress = models.CharField(max_length=100,choices=[('Not Contacted Yet', 'Not Contacted Yet'), ('Not Answering', 'Not Answering'),('Busy', 'Busy'),('Contacted', 'Contacted:Waiting For Reply'),('Got Appointment', 'Got Appointment'),('Payment', 'Payment'),('Not Interested', 'Not Interested')],default='Not Contacted Yet')
    status = models.CharField(max_length=100,choices=[('Not Answering', 'Not Answering'),('Follow Up', 'Follow Up'), ('Won', 'Won'),('Lost', 'Lost')],default='Not Answering')
    last_contacted = models.DateField(auto_now=True)
    probability = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    notes = models.TextField()
class saleperson(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    todays_lead = models.IntegerField(default=0)
    strength = models.CharField(max_length=500)
    def __str__(self):
        return self.user.first_name
class Target(models.Model):
    sale = models.ForeignKey(saleperson,on_delete=models.CASCADE,related_name='sale')
    target = models.IntegerField(default=0)
    target_won = models.IntegerField(default=0)
    target_remaining = models.IntegerField(default=0)
    date = models.DateField()
class Daily_Target(models.Model):
    sale = models.ForeignKey(saleperson,on_delete=models.CASCADE,related_name='daily_sale')
    target = models.IntegerField(default=0)
    target_won = models.IntegerField(default=0)
    target_remaining = models.IntegerField(default=0)
    date = models.DateField()
class Duty(models.Model):
    lead = models.ForeignKey(leeds,on_delete=models.CASCADE,related_name='lead')
    sale = models.ForeignKey(saleperson,on_delete=models.CASCADE,related_name='salesperson')
    won = models.CharField(max_length=3,choices=[('Yes', 'Yes'), ('No', 'No')],default='No')
    created_on = models.DateField(auto_now=True)
    delete_date = models.DateField()

class course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    internship = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    gst = models.CharField(max_length=100)
    total_rate = models.CharField(max_length=100)
    syllabus = models.FileField(upload_to='media/')
    def __str__(self):
        return self.name

class callback(models.Model):
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    date = models.DateField()
class Won(models.Model):
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE, related_name='duty')
    course = models.ForeignKey(course, on_delete=models.CASCADE, related_name='course')
    mode = models.CharField(max_length=100,choices=[('Course', 'Course'), ('Internship', 'Internship')])
    type = models.CharField(max_length=100, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    won_on = models.DateField(auto_now=True)
class payment(models.Model):
    won = models.ForeignKey(Won, on_delete=models.CASCADE, related_name='sale')
    rate = models.CharField(max_length=100)
    screenshot = models.FileField(upload_to='media/')
class Report(models.Model):
    name = models.CharField(max_length=100)
    csv = models.FileField(upload_to='report')
    created_on = models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.created_on}"