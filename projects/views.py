from django.shortcuts import redirect, render
from github_contributions import user
from blog.models import Post
from api.githubShowcase.GitHubAPI import get_data,check_github_username
from api.Users.UserManager import UserAPI
from .models import profile_register
# Create your views here.


def index(request):
    blog = Post.objects.all()[:3]
    return render(request,"projects/index.html",{"post":blog})

def profile_add(request):

    if request.method == "POST":
        get_username = request.POST.get("username")

        if check_github_username(get_username):
            if is_profile_already(get_username):
                return render(request,"projects/GitHubShowcase/add_profile.html",{"error":"Profile already exits","url":True,"user":get_username})
            else:
                add_profile = profile_register.objects.create(username=get_username)
                add_profile.save()
                return redirect("/projects/github-showcase/profile/{}".format(get_username))
        else:
            return render(request,"projects/GitHubShowcase/add_profile.html",{"error":"No such GitHub username"})
    else:
        if request.user.is_authenticated and request.user.is_active:
            return render(request,"projects/GitHubShowcase/add_profile.html")
        else:
            return render(request,"IndexHome/login.html")


def profile(request,username):
    if is_profile_already(username):
        profile_data = get_data(username)
        if profile_data is not None:
            try:
                if profile_data['RateLimits']:
                    return render(request,"config/error.html",{"error":"GitHub API Rate Limits Exceeded , try after some time"})
            except:
                return render(request,"projects/GitHubShowcase/profile.html",{"profile":profile_data,"repos_list":profile_data['repos_name']})
        else:
            return render(request,"config/error.html",{"error":"Oops somethings went wrong, please contact support"})
    else:
        return render(request,"config/error.html",{"error":"No such profile found , create-account to create one"})

def githubShowcase(request):
    pass

def is_profile_already(username):
    query = profile_register.objects.filter(username=username).exists()
    return query
