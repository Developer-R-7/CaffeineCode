# ALL IMPORTS
from django import http, template
from django.db.models.expressions import F
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseGone
from . models import Profile
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import math as m
import base64
from cryptography.fernet import Fernet
import random as r
from IndexHome.task import SendOTP


# GOBAL VAR
temp = str()


# ALL VIEWS #

def EnCrypt(email_to_encrypt):
    GEN_KEY() 
    fernet = Fernet(settings.KEY)
    encMessage = fernet.encrypt(email_to_encrypt.encode())
    encMessage = base64.urlsafe_b64encode(encMessage).decode()
    return encMessage

def DeCrypt(text_to_decrypt,key):
    fernet_de = Fernet(key)
    decMessage = base64.urlsafe_b64decode(text_to_decrypt)
    decMessage = fernet_de.decrypt(decMessage).decode()
    return decMessage
    
def check_user(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)

def OTPgen() : 
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = "" 
    varlen= len(string) 
    for i in range(6) : 
        OTP += string[m.floor(r.random() * varlen)] 
    return OTP
    
def GEN_KEY():
    key = Fernet.generate_key()
    settings.KEY = key

def verify(request,mail_hash):
    try:
        decrypt_email = DeCrypt(mail_hash,settings.KEY)
        chec_ver_user = Profile.objects.filter(user_email=decrypt_email).values_list('is_verfied',flat=True)
    except:
        return render(request,"IndexHome/error.html",{'error':"Unauthorized Access","status":"high"})
    if request.method == "POST":
            global temp
            USER_OTP_IN = request.POST.get('Passcode')
            if str(USER_OTP_IN) == str(temp):
                # CORRECT OTP
                try:
                    get_verified = Profile.objects.get(user_email=decrypt_email)
                    get_verified.is_verfied = True
                    get_verified.save()
                    GEN_KEY()
                    settings.MAX_OTP_REQUEST = 0
                    return redirect("/account/login")
                except:
                    return render(request,"IndexHome/error.html",{'error':"Verification failed user not verified Contact Support!","status":"medium"})
            else:
                if settings.MAX_OTP_REQUEST <= 3:
                    settings.MAX_OTP_REQUEST +=1
                    return render(request,"IndexHome/verify.html",{'otp_FAILED':True,'mail':mail_hash,'email':decrypt_email})
                else:
                    settings.MAX_OTP_REQUEST = 0
                    GEN_KEY()
                    return render(request,'IndexHome/error.html',{'error':"Max OTP requested. Verification failed ","status":"high"})
    else:
        if len(chec_ver_user) != 0:
            if chec_ver_user[0] is False:
                OTP_GENERATE = OTPgen()
                temp = OTP_GENERATE
                SendOTP.delay(decrypt_email,OTP_GENERATE)
                return render(request,"IndexHome/verify.html",{'email':decrypt_email,'mail':mail_hash})
            else:
                return render(request,"IndexHome/error.html",{'error':"User already verified!.","status":"medium"})
        else:
            return render(request,"IndexHome/error.html",{'error':"Oops!! Somethings went wrong. Please let us know about ,send feedback.","status":"medium"})

def check_session(request):
    return render(request,'IndexHome/check-session.html')

def index(request):
    return render(request,'IndexHome/index.html')



def test(request):
    #SendOTP.delay('rushinasa06@gmail.com',456733)
    return HttpResponse('MAIL SENT SUCCEFULLY')

def check_acc_id(id):
    query = list(Profile.objects.filter(account_id = id).values_list('account_id', flat=True))
    if len(query)  == 0:
        return True
    else:
        return False

def generate_id():
    account_id_generate = get_random_string(8, allowed_chars='0123456789')
    return account_id_generate


def resend_otp(request,mail_hash,request_otp):
    try:
        email = DeCrypt(mail_hash,settings.KEY)
    except:
        return render(request,"IndexHome/error.html",{'error':"Unauthorized request send","status":"high"})
    if settings.MAX_RESEND_CODE <=3:
        #send code
        settings.MAX_OTP_REQUEST +=1
        OTP_GEN = OTPgen()
        global temp
        temp = OTP_GEN
        SendOTP.delay(email,OTP_GEN)       
        return render(request,"IndexHome/verify.html",{'mail':mail_hash,'email':email,'resend_request':True})
    else:
        settings.MAX_RESEND_CODE = 0
        GEN_KEY()
        return render(request,'IndexHome/error.html',{'error':"Max OTP requested. Verification failed ","status":"medium"})

def signin(request):
    if request.user.is_authenticated:
        return render(request,"IndexHome/error.html",{"error":"User Already Login ","status":"low"})
    else:
        if request.method == "POST":
            try:
                sign_in_email = request.POST.get('email','default')
                sign_in_password = request.POST.get('password','default')
            except:
                return render('IndexHome/error.html',{"error":'Bypass blocked',"status":"high"})
            data_get = User.objects.filter(email = sign_in_email)
            if data_get.first() is None:
                return render(request,'IndexHome/login.html',{"error":"You don't have account linked with this mail"})
            else:
                try:
                    username = [data for data in data_get]
                    acc_id = list(Profile.objects.filter(user_email=sign_in_email).values_list('account_id', flat=True))
                    user = auth.authenticate(username = username[0] , password = sign_in_password)
                    if user is not None and user.is_active:
                        if Profile.objects.filter(user_email=sign_in_email).values_list('is_verfied',flat=True)[0] is True:
                            auth.login(request,user)
                            if request.session["is_redirect"] == True:
                                return redirect("/blog/article/{}".format(request.session["pk_to_redirect"]))
                            else:
                                return redirect('/')
                        else:
                            ver_req = EnCrypt(sign_in_email)
                            return render(request,'IndexHome/login.html',{"error":"Account not verified","verify_request":True,"mail_en":ver_req})
                    else:
                        return render(request,'IndexHome/login.html',{"error":"Incorrect email or password"}) 
                except:
                    return render(request,'IndexHome/error.html',{'error':"Error Signin ,Please contact support.","status":"medium"})           
        else:
            try:
                pk_value = request.GET.get("blog-redirect-id")
                request.session['pk_to_redirect'] = int(pk_value)
                request.session['is_redirect'] = True
            except:
                request.session['is_redirect'] = False
                pass       
            return render(request,'IndexHome/login.html')
    
def signup(request):
    if request.user.is_authenticated:
        return render(request,"IndexHome/error.html",{"error":"User Already Login","status":"low"})
    else:
        if request.method == "POST":
            try:
                data_email = request.POST.get("email")
                data_name = request.POST.get("username")
                data_pass = request.POST.get("password")
            except:
                return render(request,"IndexHome/error.html",{"error":"By Pass blocked!","status":"high"})
            try:
                if User.objects.filter(email = data_email).first():
                    return render(request,'IndexHome/signup.html',{"error":"You Already Have account linked with this mail"})
                else:
                    if User.objects.filter(username = data_name).first():
                        return render(request,'IndexHome/error.html',{"error":"Unauthorized access","status":"high"})
                    else:
                        try:
                            user_obj = User.objects.create(username = data_name ,email = data_email)
                            user_obj.set_password(data_pass)
                            user_obj.save()
                            id_generated = generate_id()
                            if check_acc_id(id_generated):
                                dat = EnCrypt(data_email)
                                profile_obj = Profile.objects.create(user = user_obj,account_id=id_generated,user_email = data_email)
                                profile_obj.save()
                                return redirect('/verify/{}'.format(dat))
                            else:
                                return render(request,'IndexHome/error.html',{"error":"Server Error Please Try again","status":"medium"})#check for same account id
                        except:
                            return render(request,'IndexHome/error.html',{'error':"Failed To create Account ,Please contact support","status":"high"})
            except:
                return render(request,'IndexHome/error.html',{'error':"Oops! Somethings went wrong ,Please contact support.","status":"high"})
        else:
            return render(request,'IndexHome/signup.html')


def logout(request):
    if request.user.is_authenticated and request.user.is_active:
        auth.logout(request)
        return render(request,'IndexHome/error.html',{"error":"Logout Successfully!","status":"low"})
    else:
        return redirect("/")



def forgot(request):
    if request.method == "POST":
        global temp
        user_found = False
        try:
            mail_to_request = request.POST.get("email")
            try:
                check = User.objects.get(email=mail_to_request)
                user_found = True
            except User.DoesNotExist:
                return render(request,'IndexHome/forgot.html',{"warning":True})
            if user_found :
                OTP_GEN_VER = OTPgen()
                temp = OTP_GEN_VER
                SendOTP.delay(mail_to_request,OTP_GEN_VER)
                request.session['email'] = mail_to_request
                return render(request,"IndexHome/forgot-final.html")
            else:
                return render(request,"IndexHome/forgot.html",{"warning":True})       
        except:
            return render(request,"IndexHome/error.html",{"error":"Failed to make forgot password request","status":"high"})
    else:
        return render(request,"IndexHome/forgot.html")

def forgot_final(request):
    try:
        mail = request.session['email']
    except KeyError:
        return render(request,'IndexHome/error.html',{"error":"Unauthorized request","status":"high"})
    if request.method == "POST":
        try:
            get_code = request.POST.get("code")
            get_new_pass = request.POST.get("password")
            global temp
            if temp == get_code:
                change_user = User.objects.get(email=mail)
                change_user.set_password(get_new_pass)
                change_user.save()
                return render(request,'IndexHome/error.html',{"error":"Your Password Changed successful","status":"low"})
            else:
                return render(request,'IndexHome/forgot-final.html',{"error":"Incorrect Verifcation code"})
        except:
            return render(request,'IndexHome/error.html',{"error":"Something went wrong Please contact support","status":"high"})
    else:
        return render(request,'IndexHome/forgot-final.html')
            