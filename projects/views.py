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

    if profile_data is not None:
        try:
            if profile_data['RateLimits']:
                return render(request,"config/error.html",{"error":"GitHub API Rate Limits Exceeded , try after some time"})
        except:
            return render(request,"projects/GitHubShowcase/profile.html",{"profile":profile_data,"repos_list":profile_data['repos_name']})
    else:
        return render(request,"config/error.html",{"error":"Oops somethings went wrong, please contact support"})

def githubShowcase(request):
    pass