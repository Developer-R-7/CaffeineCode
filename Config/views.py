from django.shortcuts import render

def maintenance(request):
    return render(request,"config/maintenance.html")

def handler500(request,*args, **argv):
    response = render(request,'config/server_error.html')
    response.status_code = 500
    return response

def handler404(request,*args, **argv):
    response = render(request,"config/error.html",{"error_code":True,"error":"404! Not Found"})
    response.status_code = 404
    return response