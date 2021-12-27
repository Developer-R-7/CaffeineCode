from django.shortcuts import render
from blog.models import Post

# Create your views here.


def index(request):
    blog = Post.objects.all()[:3]
    return render(request,"projects/index.html",{"post":blog})