from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
import json
from django.http.response import HttpResponse, HttpResponseRedirect
from numpy import size
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import uuid,random
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.contrib.auth import authenticate,login,logout

from sqlalchemy import false


otp=""
auth_token=""

# Create your views here.


def index(request):
    return render(request,"system/main.html")

def login_here(request):
    return render(request,"system/login.html")

def login_site(request):
    print(request.body)
    data=json.loads(request.body)
    username = data['username']
    password = data['password']
    try:
            user_obj=User.objects.get(username=username)
            if user_obj:
                print("exists")
                profile_obj=profile.objects.get(user=user_obj)
                if profile_obj.is_verified:
                    user=authenticate(request,username=username,password=password)
                    if user:
                        login(request,user)
                        print("done")
                        return redirect("/")
                    else:
                        print("nt login")
                else:
                    print("NOT VERIFIED")
    except:
            messages.success(request,"INVALID CREDITALS")
            return redirect('/register')

    return JsonResponse('good to do',safe=False)


def register_here(request):
    return render(request,"system/register.html")

def register_for_site(request):

    print(request.body)
    data=json.loads(request.body)
    username = data['username']
    email = data['email']
    password = data['password']

    user_obj=User.objects.create(username=username,email=email)
    user_obj.set_password(password)
    user_obj.save()
    auth_token=str(uuid.uuid4())  #storing ;random token
    profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
    profile_obj.save()
    send_email(email,auth_token)


    return JsonResponse('good to do',safe=False)


def send_email(email,auth_token):
    global otp
    initial="f-"     #authentication OTP initial
    for i in range(5):
        if i==0:
            otp=initial 
        geting_ready= str(random.randint(1,9))  
        otp=otp+geting_ready     #fianl OTP in making
    print(otp)     #OTP
    


    subject = "VERIFICATION PROCESS"
    message="YOUR VERIFICATION PASSCODE is "+ otp
    print(message)
    email_from = settings.EMAIL_HOST_USER
    email_from_pass = settings.EMAIL_HOST_PASSWORD
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(email_from, email_from_pass)
    
    # sending the mail
    s.sendmail(email_from, email,message)
    
    # terminating the session
    s.quit()
    
