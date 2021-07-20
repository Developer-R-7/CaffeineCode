from django.contrib.auth import logout
from django.urls import path

from . import views
app_name = 'IndexHome'
urlpatterns = [
    path('', views.index, name='index'),
    path('check-session/', views.check_session, name='check_session'),
    path('logout/',views.logout,name='logout'),
    path('test/',views.test,name='test'),
    path('checksessiondata/',views.check_user,name="check_user"),
    path('verify/<str:mail_hash>/',views.verify,name="verify"),
    path('verify/<str:mail_hash>/?request_otp=<str:request_otp>',views.resend_otp,name="verify_resend"),
]
