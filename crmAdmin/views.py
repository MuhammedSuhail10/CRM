from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Sum, F
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import *
import csv,io,calendar
def dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        leed = leeds.objects.all()[:4]
        sale = saleperson.objects.all()[:4]
        courses = course.objects.all()[:4]
        payments = payment.objects.all()[:4]
        callbacks = callback.objects.all().order_by('date')[:4]
        leads_won =Won.objects.annotate(month=ExtractMonth("won_on")).values("month").annotate(count=Count("id")).values("month", "count")[:3]
        return render(request,'admin/dashboard.html',{'leed':leed,'sale':sale,'course':courses,'payment':payments,'callback':callbacks,'won':leads_won})
    else:
        return redirect('admin_login')
def leed(request):
    if request.user.is_authenticated and request.user.is_superuser:
        lead = leeds.objects.all().order_by('-id')
        count = leeds.objects.all().count()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],request.user)
            return redirect('leed')
        return render(request,"admin/leed.html",{'lead':lead,'form':form,'count':count})
    else:
        return redirect('admin_login')
def handle_uploaded_file(uploaded_file,assign):
    text_file = io.TextIOWrapper(uploaded_file, encoding='utf-8')
    csv_reader = csv.reader(text_file)
    for row in csv_reader:
        name = row[0].strip()
        email = row[1].strip()
        phone = row[2].strip()
        department = row[6].strip()
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        number = cleaned_phone[2:]
        if name != 'name' and phone != 'phone':
            if leeds.objects.filter(number=number).exists():
                pass
            else:
                leads = leeds.objects.create(name=name, number=number, email=email, department=department)
                leads.save()
                person1 = saleperson.objects.all()
                count=0
                for i in person1:
                    j=0
                    for j in range(int(i.strength)):
                        if int(i.todays_lead) < int(i.strength):
                            lead = leeds.objects.get(number=number)
                            j += 1
                            if lead.assign_status == 'No':
                                thirty_days = timezone.now().date() + timedelta(days=1)
                                duty = Duty.objects.create(lead=lead,sale=i,delete_date=thirty_days)
                                duty.save()
                                i.todays_lead = int(i.todays_lead) + j
                                i.duty_on = timezone.now()
                                i.save()
                                lead.assign_status = 'Yes'
                                lead.save()
def reset_todays_leads(request):
    for i in saleperson.objects.all():
        i.todays_lead = 0
        i.save()
    for i in Daily_Target.objects.all():
        i.target_won=0
        i.target_remaining = int(i.target)
        i.save()
    for i in Duty.objects.all():
        if timezone.now().date()==i.delete_date and i.lead.lead_status =='No':
            lead=leeds.objects.get(number=i.lead.number)
            lead.assign_status = 'No'
            lead.save()
            i.delete()
    return redirect('leed')
def edit_lead(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        lead = leeds.objects.get(id=id)
        if request.method == 'POST':
            lead.name = request.POST.get('name')
            lead.number = request.POST.get('number')
            lead.email=request.POST.get('email')
            lead.watsapp = request.POST.get('wpno')
            lead.department = request.POST.get('department')
            lead.save()
            return redirect('leed')
        return render(request, "admin/edit_lead.html", {'lead': lead})
    else:
        return redirect('admin_login')
def del_lead(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        lead=leeds.objects.get(id=id)
        if Duty.objects.filter(lead=lead).exists():
            duty = Duty.objects.get(lead=lead)
            saleid = duty.sale.id
            duty.delete()
            lead.delete()
        else:
            lead.delete()
        return redirect('leed')
    else:
        return redirect('admin_login')

def lead_status(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        lead = leeds.objects.get(id=id)
        ld_status = leadstatus.objects.filter(leed=lead).order_by('-id')
        duty = Duty.objects.filter(lead=lead).first()
        if duty:
            sale = duty.sale
            calls = callback.objects.filter(duty=duty).first()
            return render(request, "admin/lead_status.html",{'lead_status':ld_status,'lead':lead,'calls':calls,'sale':sale})
        else:
            message = f"No duty have been scheduled."
            messages.error(request, message)
            return render(request,"admin/lead_status.html")
    else:
        return redirect('admin_login')
def salespersons(request):
    if request.user.is_authenticated and request.user.is_superuser:
        person1 = saleperson.objects.all().order_by('-id')
        if request.method == 'POST':
            username = request.POST.get('number')
            name = request.POST.get('name')
            email=''
            password = request.POST.get('password')
            strength = request.POST.get('strength')
            if User.objects.filter(username=username).exists():
                return redirect('salesperson')
            else:
                user = User.objects.create_user(username,email,password)
                user.first_name = name
                user.is_staff = True
                user.save()
                users = User.objects.get(username=username)
                person = saleperson.objects.create(user=users,password=password,strength=strength)
                person.save()
                target = request.POST.get('mon_tar')
                target_won = 0
                targets = Target(sale=saleperson.objects.get(user__id=users.id), target=target, target_remaining=target,
                                      target_won=target_won, date=timezone.now())
                targets.save()
                qualities = request.POST.get('daily_tar')
                target_wons = 0
                quality = Daily_Target(sale=saleperson.objects.get(user__id=users.id), target=qualities, target_remaining=qualities,
                                      target_won=target_wons, date=timezone.now())
                quality.save()
                return redirect('salesperson')
        return render(request, "admin/salespersons.html", {'person': person1})
    else:
        return redirect('admin_login')

def edit_sales(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        lead = saleperson.objects.get(id=id)
        user=lead.user
        if request.method == 'POST':
            user.first_name = request.POST.get('name')
            user.username = request.POST.get('number')
            password = request.POST.get('password')
            lead.strength = request.POST.get('strength')
            lead.password = request.POST.get('password')
            lead.target = request.POST.get('target')
            user.set_password(password)
            user.save()
            lead.save()
            return redirect('salesperson')
        return render(request, "admin/edit_sales.html", {'lead': lead})
    else:
        return redirect('admin_login')
def del_sales(request,id):
    person1 = saleperson.objects.get(id=id)
    duty=Duty.objects.filter(sale__id=id)
    for i in duty:
        lead = leeds.objects.get(id=i.lead.id)
        lead.assign_status = 'No'
        lead.save()
    duty.delete()
    u_id=person1.user.id
    user=User.objects.get(id=u_id)
    person1.delete()
    user.delete()
    return redirect('salesperson')
def duty(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        person1 = saleperson.objects.get(id=id)
        duty=Duty.objects.filter(sale=person1)
        target =Target.objects.filter(sale=person1).annotate(month=ExtractMonth("date")).values("month").annotate(target_won=Sum('target_won'),target=Sum('target'),target_remaining=F('target') - F('target_won')).values("month", "target_won","target","target_remaining")
        daily =Daily_Target.objects.filter(sale=person1).annotate(month=ExtractMonth("date")).values('month').annotate(target_won=Sum('target_won'),target=Sum('target'),target_remaining=F('target') - F('target_won')).values("date", "target_won","target","target_remaining")
        for entry in target:
            entry['month'] = get_month_name(entry['month'])
        if 'targets' in request.POST:
            person=request.POST.get('user')
            current_month = datetime.now().month
            targets = Target.objects.filter(sale=person,date__month=current_month)
            if targets.exists():
                for i in targets:
                    i.target = request.POST.get('target')
                    i.target_remaining = int(i.target) - int(i.target_won)
                    i.save()
            else:
                target = request.POST.get('target')
                target_won = 0
                target = Target(sale=saleperson.objects.get(id=person),target=target,target_remaining=target,target_won=target_won,date=timezone.now())
                target.save()
            return redirect('duty',id=id)
        if 'quality' in request.POST:
            person=request.POST.get('user')
            date = datetime.now().month
            targets = Daily_Target.objects.filter(sale=person,date__month=date)
            if targets.exists():
                for i in targets:
                    i.target = request.POST.get('qualities')
                    i.target_remaining = int(i.target) - int(i.target_won)
                    i.save()
            else:
                target = request.POST.get('qualities')
                target_won = 0
                target = Daily_Target(sale=saleperson.objects.get(id=person),target=target,target_remaining=target,target_won=target_won,date=timezone.now())
                target.save()
            return redirect('duty',id=id)
        return render(request, "admin/duty.html",{'duty':duty,'person1':person1,'data':target,'daily':daily})
    else:
        return redirect('admin_login')
def del_duty(request,id):
    duty = Duty.objects.get(id=id)
    id = duty.sale.id
    persons = saleperson.objects.get(id=id)
    persons.todays_lead = int(persons.todays_lead) - 1
    persons.save()
    lead_id = duty.lead.id
    leads = leeds.objects.get(id=lead_id)
    leads.assign_status = 'No'
    leads.save()
    duty.delete()
    return redirect('salesperson')
def courses(request):
    if request.user.is_authenticated and request.user.is_superuser:
        courses=course.objects.all().order_by('-id')
        if request.method == 'POST':
            name = request.POST.get('name')
            duration = request.POST.get('course')
            internship = request.POST.get('internship')
            base_rate = request.POST.get('rate')
            gst = request.POST.get('gst')
            total_rate=int(base_rate)+(int(base_rate)*(int(gst)/100))
            syllabus = request.FILES['syllabus']
            person = course.objects.create(name=name, duration=duration, internship=internship,rate=base_rate,gst=gst,total_rate=int(total_rate),syllabus=syllabus)
            person.save()
            return redirect('course')
        return render(request,"admin/course.html",{'courses':courses})
    else:
        return redirect('admin_login')
def del_course(request,id):
    courses = course.objects.get(id=id)
    courses.delete()
    return redirect('course')
def edit_course(request,id):
    courses=course.objects.get(id=id)
    if request.method == 'POST':
        courses.name = request.POST.get('name')
        courses.duration = request.POST.get('duration')
        courses.internship = request.POST.get('internship')
        courses.rate = request.POST.get('rate')
        courses.gst = request.POST.get('gst')
        total_rate = int(courses.rate)+(int(courses.rate)*(int(courses.gst)/100))
        courses.total_rate=int(total_rate)
        if 'check' in request.POST:
            courses.syllabus = request.FILES['syllabus']
        courses.save()
        return redirect('course')
    return render(request,'admin/edit_course.html',{'courses':courses})
def payments(request):
    if request.user.is_authenticated and request.user.is_superuser:
        payments = payment.objects.all()
        return render(request,"admin/payment.html",{'payments':payments})
    else:
        return redirect('admin_login')
def del_pay(request,id):
    payments = payment.objects.get(id=id)
    payments.delete()
    return redirect('payments')
def callbacks(request):
    if request.user.is_authenticated and request.user.is_superuser:
        calls = callback.objects.all()
        return render(request,"admin/callback.html",{'calls':calls})
    else:
        return redirect('admin_login')
def assign(request):
    if request.user.is_authenticated and request.user.is_superuser:
        assign = leeds.objects.filter(assign_status='No')
        count = leeds.objects.filter(assign_status='No').count()
        return render(request,"admin/assign_duty.html",{'assign':assign,'count':count})
    else:
        return redirect('admin_login')
def assign_lead(request,id):
    person1 = saleperson.objects.all()
    for i in person1:
        j = 0
        for j in range(int(i.strength)):
            if int(i.todays_lead) < int(i.strength):
                lead = leeds.objects.get(id=id)
                j += 1
                if lead.assign_status == 'No':
                    thirty_days = timezone.now().date() + timedelta(days=30)
                    duty = Duty.objects.create(lead=lead, sale=i, delete_date=thirty_days)
                    duty.save()
                    i.todays_lead = int(i.todays_lead) + j
                    i.duty_on = timezone.now()
                    i.save()
                    lead.assign_status = 'Yes'
                    lead.save()
    return redirect(assign)
def won(request):
    if request.user.is_authenticated and request.user.is_superuser:
        won = Won.objects.all()
        return render(request, "admin/leads_won.html",{'won':won})
    else:
        return redirect('admin_login')
def settings(request):
    superusers = User.objects.filter(is_superuser=True)
    if 'name' in request.POST:
        id = request.POST.get('id')
        user=User.objects.get(id=id)
        user.username = request.POST.get('username')
        user.save()
        return redirect('settings')
    if 'fname' in request.POST:
        ids = request.POST.get('id')
        users=User.objects.get(id=ids)
        users.first_name = request.POST.get('names')
        users.save()
        return redirect('settings')
    if 'pass' in request.POST:
        idss = request.POST.get('id')
        userspass=User.objects.get(id=idss)
        password = request.POST.get('password')
        userspass.set_password(password)
        userspass.save()
        return redirect('admin_login')
    if 'addadmin' in request.POST:
        usernames = request.POST.get('usernames')
        password = request.POST.get('passwords')
        user_inp= User.objects.create_user(username=usernames,password=password)
        user_inp.is_superuser = True
        user_inp.first_name = request.POST.get('f_name')
        user_inp.save()
        return redirect('settings')
    return render(request, "admin/settings.html",{'superusers':superusers})
def edit_admin(request,id):
    user = User.objects.get(id=id)
    if request.method=='POST':
        user.first_name=request.POST.get('name')
        user.username=request.POST.get('username')
        password=request.POST.get('password')
        user.set_password(password)
        user.save()
        return redirect('settings')
    return render(request,'admin/edit_admin.html', {'user': user})
def del_suser(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('settings')
def followup(request):
    if request.user.is_authenticated and request.user.is_superuser:
        duty = Duty.objects.filter(lead__lead_status='Yes').order_by('-created_on')
        list =[]
        for i in duty:
            leads = leadstatus.objects.filter(leed=i.lead).last()
            if leads:
                list.append(leads)
        return render(request, 'admin/followups.html', {'duty': list})
    else:
        return redirect('admin_login')
def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('mobile')
        password=request.POST.get('pass')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dash')
        else:
            return redirect('admin_login')
    return render(request,'admin/login.html')
def logoutpage(request):
    logout(request)
    return redirect('admin_login')
def get_month_name(month_number):
    return calendar.month_name[month_number]
