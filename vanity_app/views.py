from email import errors

from django.shortcuts import render, redirect
from .models import User, Service, Class, Appointment
from django.contrib import messages
import bcrypt
import datetime
from django.utils import timezone


def home(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

def login_page(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            current_user = User.objects.get(id=request.session['user_id'])
            return redirect(f'/account/{user.id}')
    messages.error(request, "Email or password is incorrect")
    return redirect('/login_page')

def not_logged(request):
    messages.error(request, "You must be logged in first!")
    return redirect('/login_page')

def logout(request):
    request.session.clear()
    return redirect('/')

def register_page(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("there are errors")
            return redirect('/register_page')
        else:
            if request.method == "POST":
                hashed_pw = bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt()).decode()
                user = User.objects.create(
                    first_name=request.POST['first_name'], last_name=request.POST['last_name'], phone_number=request.POST['phone_number'], email=request.POST['email'], password=hashed_pw)
                request.session['user_id'] = user.id
                print(User.objects.get(id=user.id))
            return redirect(f'/account/{user.id}')
    return redirect('/')

def services(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'all_services': Service.objects.all()
        }
        return render(request, 'services.html', context)
    else:
        context = {
            'all_services': Service.objects.all()
        }
        return render(request, 'services.html', context)


def service_info(request, service_id):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'a_service': Service.objects.get(id=service_id)
        }
        return render(request, 'service_details.html', context)
    else:
        context = {
            'a_service': Service.objects.get(id=service_id)
        }
        return render(request, 'service_details.html', context)

def book_service(request, service_id):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id']),
            'a_service': Service.objects.get(id=service_id)
        }
        user_id = request.session['user_id']
        current_user = User.objects.get(id=request.session['user_id']),
        a_service = Service.objects.get(id=service_id)

        t1 = datetime.datetime.strptime(request.POST['date'], "%Y-%m-%d %H:%M:%S")
        current_tz = timezone.get_current_timezone()
        t2 = current_tz.localize(t1)

        request.POST['date']

        new_appt = Appointment.objects.create(date=t2, booked_user=User.objects.get(
            id=request.session['user_id']), service=Service.objects.get(id=service_id))

        return redirect(f'/account/{user_id}', context)
    else:
        context = {
            'a_service': Service.objects.get(id=service_id)
        }
        return redirect(f'/account/{user_id}', context)

def cancel_appt(request, user_id, appt_id):

    appts = Appointment.objects.filter(booked_user=User.objects.get(id=user_id))
    c = appts.get(id=appt_id)
    c.delete()

    return redirect(f'/account/{user_id}')

def classes(request):
    if 'user_id' in request.session:
        context = {
            'current_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'classes.html', context)
    else:
        return render(request, 'classes.html')


def user_account(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to log in !")
        return redirect('/login_page')
    else:
        context = {
            'current_user': User.objects.get(id=user_id),
            'user_appts': User.objects.get(id=user_id).appointments.all()
        }

        return render(request, 'my_account.html', context)
