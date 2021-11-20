# ALL IMPORTS
from django.db.models.expressions import F
from django.http.response import HttpResponse
from . models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.conf import settings
from main_api_handlers.Profiles.VerifyManager import profile_manager
from cryptography.fernet import Fernet
from IndexHome.task import SendOTP


# GOBAL VAR
temp = str()


# ALL VIEWS #

def EnCrypt(message: bytes, key: bytes):
    return Fernet(key).encrypt(message)

def DeCrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)
    
    
def check_user(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def verify(request,mail_hash,id):
    try:
        verify_manager = profile_manager()
        get_user = verify_manager.search_user_with_id(id)
        decrypt_email = DeCrypt(mail_hash.encode('utf-8'),get_user.key.encode('utf-8')) #this is a bytes
        is_user_verify = verify_manager.is_user_verify(decrypt_email)
    except:
        return render(request,"IndexHome/error.html",{'error':"Unauthorized Access ","status":"high"})
    if request.method == "POST":
            USER_OTP_IN = request.POST.get('Passcode')
            if verify_manager.verify_otp(id,USER_OTP_IN):
                # CORRECT OTP
                try:
                    verify_manager.update_verify(id)
                    #verify_manager.delete_field(id)
                    #login user here
                    return redirect("/dashboard/home")
                except:
                    return render(request,"IndexHome/error.html",{'error':"Verification failed user not verified Contact Support!","status":"medium"})
            else:
                if verify_manager.get_fail(id) <= 3:
                    verify_manager.add_fail_request(id)
                    return render(request,"IndexHome/verify.html",{'otp_FAILED':True,'mail':mail_hash,'email':decrypt_email,"id":id})
                else:
                    verify_manager.reset_fail(id)
                    return render(request,'IndexHome/error.html',{'error':"Max OTP requested. Verification failed ","status":"high"})
    else:
        if is_user_verify:
            return render(request,"IndexHome/error.html",{'error':"User already verify!","status":"medium"})
        else:
            #sendmail here
            return render(request,"IndexHome/verify.html",{'email':decrypt_email,'mail':mail_hash,'id':id})
            

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


def resend_otp(request,mail_hash,acc_id,request_otp):
    if request_otp:
        try:
            verify_manager = profile_manager()
            get_user = verify_manager.search_user_with_id(acc_id)
            email = DeCrypt(mail_hash.encode('utf-8'),get_user.key.encode('utf-8'))
        except:
            return render(request,"IndexHome/error.html",{'error':"Unauthorized request send","status":"high"})
        if get_user.resend_request <=3:
            verify_manager.generate_only_otp(acc_id)
            #Sendmail here      
            return render(request,"IndexHome/verify.html",{'mail':mail_hash,'email':email,'resend_request':True,'id':acc_id})
        else:
            verify_manager.reset_resend(acc_id)
            return render(request,'IndexHome/error.html',{'error':"Max OTP requested. Verification failed ","status":"medium"})
    else:
        raise Exception("false request")


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
                                return redirect('/dashboard/home')
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
            #try:
            if User.objects.filter(email = data_email).first():
                return render(request,'IndexHome/signup.html',{"error":"You Already Have account linked with this mail"})
            else:
                if User.objects.filter(username = data_name).first():
                    return render(request,'IndexHome/error.html',{"error":"Unauthorized access","status":"high"})
                else:
                    #try:
                    user_obj = User.objects.create(username = data_name ,email = data_email)
                    user_obj.set_password(data_pass)
                    user_obj.save()
                    id_generated = generate_id()
                    if check_acc_id(id_generated):
                        verify_handler = profile_manager()
                        verify_handler.createProfile(user_obj,id_generated,data_email)
                        verify_handler.add_otp(id_generated)
                        get_user = verify_handler.search_user_with_id(id_generated)
                        encrypted = EnCrypt(data_email.encode(),get_user.key.encode('utf-8'))
                        return redirect('/verify/{}/{}/'.format(encrypted.decode('utf-8'),id_generated))
                    else:
                        return render(request,'IndexHome/error.html',{"error":"Server Error Please Try again","status":"medium"})#check for same account id
                    #except:
                        #return render(request,'IndexHome/error.html',{'error':"Failed To create Account ,Please contact support","status":"high"})
            #except:
                #return render(request,'IndexHome/error.html',{'error':"Oops! Somethings went wrong ,Please contact support.","status":"high"})
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
                SendOTP(mail_to_request,OTP_GEN_VER)
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


def playground_timer(request):
    return render(request,"IndexHome/playground.html")
            