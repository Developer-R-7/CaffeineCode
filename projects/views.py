from django.shortcuts import redirect, render
from blog.models import Post
from api.githubShowcase.GitHubAPI import get_data,check_github_username
from .models import profile_register
from django.contrib.auth.models import User
import json
# Create your views here.


def index(request):
    blog = Post.objects.all()[:3]
    return render(request,"projects/index.html",{"post":blog})

def profile_add(request):

    if request.method == "POST":
        if request.user.is_authenticated and request.user.is_active:
            get_username = request.POST.get("username")
            if check_github_username(get_username):
                if is_profile_already(get_username):
                    return render(request,"projects/GitHubShowcase/add_profile.html",{"error":"Profile already exits","url":True,"user":get_username})
                else:
                    add_profile = profile_register.objects.create(github_username=get_username,user=request.user.username)
                    add_profile.save()
                    return redirect("/projects/github-showcase/profile/{}".format(get_username))
            else:
                return render(request,"projects/GitHubShowcase/add_profile.html",{"error":"No such GitHub username"})
        else:
            return render(request,"config/error.html",{"error":"By pass blocked"})
    else:
        if request.user.is_authenticated and request.user.is_active:
            if is_user_created_profile(request.user.username):
                return render(request,"config/error.html",{"error":"You can only create one profile with one account"})
            else:
                return render(request,"projects/GitHubShowcase/add_profile.html")
        else:
            return redirect("/account/login/?redirect-url={}".format(request.get_full_path()))


def profile(request,username):
    if is_profile_already(username):
        try:
            if request.COOKIES['profile_data']:
                profile_data = json.loads(request.COOKIES['profile_data'])
                response = render(request,"projects/GitHubShowcase/profile.html",{"profile":profile_data,"repos_list":profile_data['repos_name']})
        except:
            profile_data = get_data(username)
            response = render(request,"projects/GitHubShowcase/profile.html",{"profile":profile_data,"repos_list":profile_data['repos_name']})
            response.set_cookie(key='profile_data', value=json.dumps(profile_data),max_age=1800)

        if profile_data is not None:
            try:
                if profile_data['RateLimits']:
                    return render(request,"config/error.html",{"error":"GitHub API Rate Limits Exceeded , try after some time"})
            except:
                return response
        else:
            return render(request,"config/error.html",{"error":"Oops somethings went wrong, please contact support"})
    else:
        return render(request,"config/error.html",{"error":"No such profile found , create-account to create one"})

def githubShowcase(request):
    return render(request,'projects/GitHubShowcase/index.html')

def is_profile_already(github_username):
    query = profile_register.objects.filter(github_username=github_username).exists()
    return query

def is_user_created_profile(username):
    query = profile_register.objects.filter(user=username).exists()
    return query