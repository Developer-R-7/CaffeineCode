from django.urls import path

from . import views
app_name = 'IndexHome'
urlpatterns = [
    path('', views.index, name='index'),
    path('check-session/', views.check_session, name='check_session'),
    path('test/',views.test,name='test'),
    path('checksessiondata/',views.check_user,name="check_user"),
    path('verify/<str:mail_hash>/',views.verify,name="verify"),# merging request_otp url 
    path('verify/<str:mail_hash>/?request_otp=<str:request_otp>',views.resend_otp,name="verify_resend"),
    path('account/login/',views.signin,name="signin"),
    path('account/create/',views.signup,name="signup"),
    path('account/logout/',views.logout,name="logout"),
    path('account/forgot/',views.forgot,name="forgot"),
    path('account/forgot/verify',views.forgot_final,name="forgot_final"),
    path('playground/',views.playground_timer,name="playground"),
]
