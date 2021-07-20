from django.http.response import HttpResponse
from django.shortcuts import render
# Create your views here.

def dashboard(request,account_id):
    user_email = request.session.get('email')
    verify_acc_current_user = request.session.get('account_id')
    if verify_acc_current_user == account_id:
        return render(request,'dashboard/dashboard.html',{'spectator':False})
    else:
        return render(request,'dashboard/dashboard.html',{'spectator':True})