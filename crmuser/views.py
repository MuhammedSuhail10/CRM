from datetime import timedelta, datetime

from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from django.shortcuts import render, redirect
from crmAdmin.models import *


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        user = request.user
        sale = saleperson.objects.filter(user=user).first()
        duty = Duty.objects.filter(sale=sale, lead__lead_status='No').order_by('-created_on')[:4]
        calls = callback.objects.filter(duty__sale=sale)[:4]
        courses = course.objects.all()
        callbacks = callback.objects.filter(duty__sale=sale).count()
        total_duty = Duty.objects.filter(sale=sale).count()
        total_won = Won.objects.filter(duty__sale=sale).count()
        completed = Duty.objects.filter(sale=sale, lead__lead_status='Yes').count()
        uncompleted = Duty.objects.filter(sale=sale, lead__lead_status='No').count()
        wons = Duty.objects.filter(sale=sale, lead__lead_status='Won').count()
        leads_won = Won.objects.filter(duty__sale=sale).annotate(month=ExtractMonth("won_on")).values("month").annotate(
            count=Count("id")).values("month", "count")[:3]
        for i in callback.objects.filter(duty__sale=sale):
            if i.date == timezone.now().date():
                message = f"You have a callback scheduled for today . Lead : {i.duty.lead.number}"
                messages.error(request, message)
        current_month = datetime.now().month
        target = Target.objects.filter(sale=sale, date__month=current_month).first()
        daily = Daily_Target.objects.filter(sale=sale, date=datetime.now()).first()
        yesterday = Daily_Target.objects.filter(sale=sale, date__month=current_month).first()
        return render(request, 'user/index.html',
                      {'duty': duty, 'calls': calls, 'courses': courses, 'completed': completed,'l_won':wons,'daily':daily,
                       'uncompleted': uncompleted, 'won': leads_won,'total_duty':total_duty,'callbacks':callbacks,'total_won':total_won,'target':target,'yesterday':yesterday})
    else:
        return redirect('user_login')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('mobile')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('user_login')
    return render(request, 'user/login.html')


def lead(request):
    if request.user.is_authenticated and request.user.is_staff:
        user = request.user
        sale = saleperson.objects.filter(user=user).first()
        duty = Duty.objects.filter(sale=sale, lead__lead_status='No').order_by('-created_on')
        if request.method == 'POST':
            name = request.POST.get('name')
            number = request.POST.get('number')
            if leeds.objects.filter(number=number).exists():
                dut = Duty.objects.get(lead__number=number)
                message = f"Lead already exists. Asssigned to : {dut.sale}"
                messages.error(request, message)
                return redirect('lead')
            else:
                leads = leeds.objects.create(name=name, number=number,assign_status='Yes')
                leads.save()
                thirty_days = timezone.now().date() + timedelta(days=1)
                duty = Duty.objects.create(sale=sale, lead=leeds.objects.get(number=number), delete_date=thirty_days)
                duty.save()
                return redirect('lead')
        return render(request, 'user/leads.html', {'duty': duty})
    else:
        return redirect('user_login')


def status(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        lead = leeds.objects.get(id=id)
        status = leadstatus.objects.filter(leed__id=id).order_by('-last_contacted')
        courses = course.objects.all()
        payments = payment.objects.filter(won__duty__lead=lead)
        if 'statuses' in request.POST:
            leed = lead
            watsapp = request.POST.get('wp')
            progress = request.POST.get('progress')
            stats = request.POST.get('status')
            notes = request.POST.get('notes')
            probability = request.POST.get('probability')
            person = leadstatus.objects.create(leed=leed, status=stats, progress=progress, notes=notes,
                                               probability=probability, watsapp=watsapp)
            person.save()
            if stats == 'Follow Up':
                duty = Duty.objects.get(lead=leed)
                date = request.POST.get('date')
                p = leadstatus.objects.filter(leed=leed).last()
                p.course = request.POST.get('courses')
                p.save()
                if callback.objects.filter(duty=duty).exists():
                    callbacks = callback.objects.get(duty=duty)
                    callbacks.delete()
                else:
                    pass
                calls = callback.objects.create(duty=duty, date=date)
                calls.save()
                leed.lead_status = 'Yes'
                leed.save()
                sale = saleperson.objects.get(user=request.user)
                k = Daily_Target.objects.filter(sale=sale, date=datetime.now()).first()
                if k:
                    k.target_won = int(k.target_won) + 1
                    k.target_remaining = int(k.target) - int(k.target_won)
                    k.save()
                else:
                    current_month = datetime.now().month
                    v = Daily_Target.objects.filter(sale=sale, date__month=current_month).first()
                    target_won = int(v.target_won) + 1
                    target_remaining = int(v.target) - int(v.target_won)
                    tar = Daily_Target.objects.create(sale=sale, date=datetime.now(), target=v.target, target_won=target_won,target_remaining=target_remaining)
                    tar.save()
            elif stats == 'Won':
                leed.lead_status = 'Won'
                leed.save()
                duty = Duty.objects.get(lead=leed)
                c = request.POST.get('course')
                courses = course.objects.get(name=c)
                mode = request.POST.get('mode')
                type = request.POST.get('type')
                won = Won.objects.create(duty=duty, course=courses, mode=mode,type=type)
                won.save()
                wons = Won.objects.get(duty=duty)
                rate = request.POST.get('rate')
                screenshot = request.FILES['ss']
                payments = payment.objects.create(won=wons, rate=rate, screenshot=screenshot)
                payments.save()
                current_month = datetime.now().month
                user = request.user
                sale = saleperson.objects.get(user=user)
                i = Target.objects.filter(sale=sale, date__month=current_month).first()
                if i:
                    i.target_won = int(i.target_won) + int(courses.rate)
                    i.target_remaining = int(i.target) - int(i.target_won)
                    i.save()
                k = Daily_Target.objects.filter(sale=sale, date=datetime.now()).first()
                if k:
                    k.target_won = int(k.target_won) + 1
                    k.target_remaining = int(k.target) - int(k.target_won)
                    k.save()
                else:
                    current_month = datetime.now().month
                    v = Daily_Target.objects.filter(sale=sale, date__month=current_month).first()
                    target_won = int(v.target_won) + 1
                    target_remaining = int(v.target) - int(v.target_won)
                    tar = Daily_Target.objects.create(sale=sale, date=datetime.now(), target=v.target, target_won=target_won,target_remaining=target_remaining)
                    tar.save()
            elif stats == 'Lost':
                leed.delete()
                return redirect('lead')
            return redirect('status', id=id)
        return render(request, "user/leadstatus.html",
                      {'leed': lead, 'status': status, 'course': courses, 'payment': payments})
    else:
        return redirect('user_login')


def del_payment(request, id):
    payments = payment.objects.get(id=id)
    payments.delete()
    leed = payment.won.duty.lead
    leed.lead_status = 'Won'
    leed.save()
    return redirect('lead')

def followups(request):
    if request.user.is_authenticated and request.user.is_staff:
        user = request.user
        sale = saleperson.objects.filter(user=user).first()
        duty = Duty.objects.filter(sale=sale, lead__lead_status='Yes').order_by('-created_on')
        list =[]
        for i in duty:
            leads = leadstatus.objects.filter(leed=i.lead).last()
            if leads:
                list.append(leads)
        return render(request, 'user/followups.html', {'duty': list})
    else:
        return redirect('user_login')


def leads_won(request):
    if request.user.is_authenticated and request.user.is_staff:
        user = request.user
        sale = saleperson.objects.filter(user=user).first()
        won = Won.objects.filter(duty__sale=sale)
        return render(request, 'user/won.html', {'duty': won})
    else:
        return redirect('user_login')


def callbacks(request):
    if request.user.is_authenticated and request.user.is_staff:
        calls = callback.objects.filter(duty__sale__user=request.user).order_by('date')
        return render(request, 'user/callbacks.html', {'calls': calls})
    else:
        return redirect('user_login')


def syllabus(request):
    if request.user.is_authenticated and request.user.is_staff:
        courses = course.objects.all()
        return render(request, 'user/syllabus.html', {'courses': courses})
    else:
        return redirect('user_login')

def logoutuser(request):
    logout(request)
    return redirect('user_login')
