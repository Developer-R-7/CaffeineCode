from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    return HttpResponse("<h1>This Is dashbaord</h1>")
