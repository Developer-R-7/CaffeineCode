from django.http.response import HttpResponse
from django.shortcuts import render
from blog.models import Post
from api.githubShowcase.GitHubAPI import get_data
# Create your views here.


def index(request):
    blog = Post.objects.all()[:3]
    return render(request,"projects/index.html",{"post":blog})

def profile_add(request):
    return HttpResponse("Hello add")

def profile(request,username):
    profile_data = get_data(username)
    return render(request,"projects/GitHubShowcase/profile.html",{"profile":profile_data})