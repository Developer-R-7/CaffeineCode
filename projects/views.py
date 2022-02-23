from django.shortcuts import redirect, render
from blog.models import Post

import json


def index(request):
    blog = Post.objects.all()[:3]
    return render(request,"projects/index.html",{"post":blog,'redirect_url':request.get_full_path()})
