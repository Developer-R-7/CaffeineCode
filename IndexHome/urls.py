from django.urls import path
from . import views

app_name = 'IndexHome'


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'check-user/', views.check_user, name="check_user"),
    path(r'verify/<str:mail_hash>/<int:id>/', views.verify,name="verify"),
    path(r'verify/<str:mail_hash>/<int:acc_id>/?request_otp=<str:request_otp>',views.resend_otp, name="verify_resend"),
    path(r'account/login/', views.signin, name="signin"),
    path(r'account/create/', views.signup, name="signup"),
    path(r'account/logout/', views.logout, name="logout"),
    path(r'account/forgot/', views.forgot, name="forgot"),
    path(r'account/forgot/verify', views.forgot_final, name="forgot_final"),
    path(r'playground/', views.playground_timer, name="playground"),
    path(r'subscribe-newsletter/',views.newsletter,name="newsletter"),
    path(r'privacy-policy/',views.privacyPolicy,name="privacy"),
    path(r'contact-us/',views.contact,name="contact"),
]
