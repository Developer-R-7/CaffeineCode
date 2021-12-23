# ALL IMPORTS
from . models import Newsletter , Notify
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from blog.models import Post,Category
from api.Users.UserManager import UserAPI
from api.Profiles.ProfileManager import profile_manager
from api.Config.error import error_message
# CLIENT-SIDE FUNCTIONS
def check_user(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


# VERIFY FUNCTIONS
def verify(request, mail_hash, id):
    try:
        profile_connector = profile_manager()
        get_user = profile_connector.search_user_with_id(id)
        decrypt_email = profile_connector.get_decrypted_string(mail_hash.encode('utf-8'),id)
        is_user_verify = profile_connector.is_user_verify(decrypt_email)
    except:
        return render(request, "config/error.html", {'error': error_message[0]})
    if request.method == "POST":
        USER_OTP_IN = request.POST.get('Passcode')
        if profile_connector.verify_otp(id, USER_OTP_IN):
            # CORRECT OTP
            try:
                profile_connector.update_verify(id)
                # None delete_field(id)
                # login user here
                return redirect("/dashboard/home")
            except:
                return render(request, "config/error.html", {'error': error_message[15]})
        else:
            if profile_connector.get_fail(id) < 3:
                profile_connector.add_fail_request(id)
                return render(request, "IndexHome/verify.html", {'otp_FAILED': True, 'mail': mail_hash, 'email': decrypt_email.decode(), "id": id})
            else:
                profile_connector.reset_fail(id)
                return render(request, 'config/error.html', {'error': error_message[13]})
    else:
        if is_user_verify:
            return render(request, "config/error.html", {'error': error_message[14]})
        else:
            try:
                get_request_from_main = request.session['main_verify']
                if get_request_from_main:
                    profile_connector.generate_only_otp(id)
                    return render(request, "IndexHome/verify.html", {'email': decrypt_email.decode(), 'mail': mail_hash, 'id': id})
                else:
                    return render(request, "IndexHome/verify.html", {'email': decrypt_email.decode(), 'mail': mail_hash, 'id': id})

            except:
                return render(request, "IndexHome/verify.html", {'email': decrypt_email.decode(), 'mail': mail_hash, 'id': id})

def resend_otp(request, mail_hash, acc_id, request_otp):
    if request_otp:
        try:
            profile_connector = profile_manager()
            get_user = profile_connector.search_user_with_id(acc_id)
            email = profile_connector.get_decrypted_string(mail_hash.encode('utf-8'),acc_id)
        except:
            return render(request, "config/error.html", {'error':error_message[0]})
        if get_user.resend_request < 3:
            profile_connector.generate_only_otp(acc_id)
            profile_connector.resend_request(acc_id)
            return render(request, "IndexHome/verify.html", {'mail': mail_hash, 'email': email.decode('utf-8'), 'resend_request': True, 'id': acc_id})
        else:
            profile_connector.reset_resend(acc_id)
            return render(request, 'config/error.html', {'error': error_message[1]})
    else:
        raise Exception("false request")


# USER FORM ACTION
@never_cache
def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            try:
                sign_in_email = request.POST.get('email', 'default')
                sign_in_password = request.POST.get('password', 'default')
                user_connector = UserAPI()
            except:
                return render('config/error.html', {"error": error_message[2]})
    
            if user_connector.is_user_has_account(sign_in_email) is False:
                return render(request, 'IndexHome/login.html', {"error": error_message[3],"create_account":True})
            else:
                try:
                    user = auth.authenticate(username=user_connector.get_username(sign_in_email), password=sign_in_password)
                    if user is not None and user.is_active:
                        if user_connector.is_user_verify(sign_in_email):
                            auth.login(request, user)
                            if request.session["is_redirect"] == True:
                                return redirect("/blog/article/{}".format(request.session["pk_to_redirect"]))
                            else:
                                return redirect('/dashboard/home')
                        else:
                            get_user = user_connector.search_user_with_account_mail(sign_in_email)
                            ver_req = user_connector.get_encrypted_string(sign_in_email,user_connector.get_key(get_user.account_id))
                            request.session['main_verify'] = True
                            return render(request, 'IndexHome/login.html', {"error": error_message[4], "verify_request": True, "mail_en": ver_req.decode('utf-8'), "id": get_user.account_id})
                    else:
                        return render(request, 'IndexHome/login.html', {"error": error_message[5]})
                except:
                    return render(request, 'config/error.html', {'error': error_message[6]})
        else:
            try:
                pk_value = request.GET.get("blog-redirect-id")
                request.session['pk_to_redirect'] = int(pk_value)
                request.session['is_redirect'] = True
            except:
                request.session['is_redirect'] = False
                pass
            return render(request, 'IndexHome/login.html')

@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            try:
                data_email = request.POST.get("email")
                data_name = request.POST.get("username")
                data_pass = request.POST.get("password")
                user_connector = UserAPI()
            except:
                return render(request, "config/error.html", {"error": error_message[2]})
            try:
                if user_connector.is_user_has_account(data_email):
                    return render(request, 'IndexHome/signup.html', {"error": error_message[7]})
                else:
                    if user_connector.check_same_username(data_name):
                        return render(request, 'config/error.html', {"error": error_message[0]})
                    else:
                        get_params = user_connector.create_account(data_name,data_email,data_pass)
                        return redirect('/verify/{}/{}/'.format(get_params[0].decode('utf-8'),get_params[1]))
            except:
                return render(request,'config/error.html',{'error':error_message[8]})
        else:
            return render(request, 'IndexHome/signup.html')

def logout(request):
    if request.user.is_authenticated and request.user.is_active:
        auth.logout(request)
        return render(request,'IndexHome/index.html',{"toast":True,"toast_mssg":"Logout Successfully!!"})
    else:
        return redirect("/")

def forgot(request):
    if request.method == "POST":
        try:
            user_connector = UserAPI()
            mail_to_request = request.POST.get("email")
            get_user_id = (user_connector.search_user_with_account_mail(mail_to_request)).account_id
            if user_connector.is_user_has_account(mail_to_request):
                if user_connector.is_user_verify(mail_to_request):
                    user_connector.generate_only_otp(get_user_id)
                    request.session['email'] = mail_to_request
                    return render(request, "IndexHome/forgot-final.html")
                else:
                    return render(request, 'IndexHome/forgot.html', {"warning": True, "message": error_message[9]})
            else:
                return render(request, "IndexHome/forgot.html", {"warning": True, "message": error_message[3]})
        except:
            return render(request, "config/error.html", {"error": error_message[16]})
    else:
        return render(request, "IndexHome/forgot.html")

def forgot_final(request):
    try:
        mail = request.session['email']
    except KeyError:
        return render(request, 'config/error.html', {"error":error_message[0]})
    if request.method == "POST":
        try:
            get_code = request.POST.get("code")
            get_new_pass = request.POST.get("password")
            user_connector = UserAPI()
            get_user = user_connector.search_user_with_account_mail(mail)
            if user_connector.verify_otp(get_user.account_id,get_code):
                user_connector.set_user_password(mail,get_new_pass)
                return render(request, 'IndexHome/index.html', {"toast":True,"toast_mssg": error_message[10]})
            else:
                return render(request, 'IndexHome/forgot-final.html', {"error": error_message[11]})
        except:
            return render(request, 'config/error.html', {"error": error_message[12]})
    else:
        return render(request, 'IndexHome/forgot-final.html')


# MAIN FUNCTION
def playground_timer(request):
    if request.method == "POST":
        try:
            get_mail = request.POST.get("notify_mail")
            obj = Notify.objects.create(notify_mail=get_mail)
            obj.save()
            return render(request,'IndexHome/playground.html',{"toast":True,"toast_mssg":"Notify register successful!"})
        except:
            return render(request,'config/error.html',{"error":error_message[17]})
    else:
        return render(request, "IndexHome/playground.html")

def index(request):
    recent_blog = Post.objects.all()
    user_count = User.objects.count()
    category = Category.objects.all()[:6]
    return render(request, 'IndexHome/index.html',{'post':recent_blog.order_by('-likes_count','-date_published')[:3],'user_count':user_count,'total_blogs':recent_blog.count(),'category':category})

def newsletter(request):
    if request.method == "POST":
        mail_to_add = request.POST.get('newsletter', None)
        if Newsletter.objects.filter(subscribe_mail=mail_to_add).exists():
            return redirect('/')
        else:
            query = Newsletter.objects.create(subscribe_mail=mail_to_add)
            query.save()
            dict = {"success":True}
            return render(request,'IndexHome/index.html',{"toast":True,"toast_mssg":"Newsletter Subscribed!!"})
    else:
        mail = request.GET.get('newsletter', None)
        query = Newsletter.objects.filter(subscribe_mail__exact=mail).exists()
        response = {
            'is_subscribe': query 
        }
        return JsonResponse(response)