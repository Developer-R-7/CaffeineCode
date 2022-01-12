from django.shortcuts import render

def maintenance(request):
    return render(request,"config/maintenance.html")

def handler500(request):
    response = render(request,'config/server_error.html')
    response.status_code = 500
    return response