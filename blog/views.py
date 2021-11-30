from typing import ContextManager
from django.core import paginator
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Post, Category
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator
import datetime
from django.db.models import Q
from hitcount.views import HitCountDetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from api.Blog.BlogManager import PostAPI
# Create your views here.


class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = ['-date_published', '-hit_count_generic__hits']
    paginate_by = 5
    def get_context_data(self, **kwargs):
        blog_connector = PostAPI()
        context = super(HomeView, self).get_context_data(**kwargs)
        context['editor'] = blog_connector.get_editor_post()
        context['most_used_tag'] = blog_connector.get_most_tags_used()
        context['trending_post'] = blog_connector.get_most_viewed()
        context['this_month'] = blog_connector.get_this_month()
        context['category'] = blog_connector.get_category()
        return context


def search_sys(request):
    if request.method == "GET":
        query = request.GET.get('search_query')
        posts = Post.objects.filter(Q(title__icontains=query) | Q(
            body__icontains=query) | Q(blog_snipet__icontains=query)).order_by('-modified')
        most_like_post = Post.objects.all().order_by('-likes_count')[:5]
        cat = Category.objects.all()[:6]
        return render(request, 'blog/search.html', {'query': query, 'result': posts, 'most_liked': most_like_post, 'category': cat})


def newsletter(request):
    if request.method == "POST":
        mail = request.POST.get("newsletter")
    else:
        return redirect('/blog/')


@login_required(login_url='IndexHome:index')
def like_sys(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == "POST":
            result = ''
            pk_value = int(request.POST.get("postid"))
            post = get_object_or_404(Post, id=pk_value)
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                post.likes_count -= 1
                result = post.likes_count
                post.save()
            else:
                post.likes.add(request.user)
                post.likes_count += 1
                result = post.likes_count
                post.save()
            return JsonResponse({"result": result, })
    else:
        return HttpResponseRedirect("/blog/")


def post_by_tags(request, tag_slug):
    most_used_tags = Post.tags.most_common()[:6]
    try:
        tag = get_object_or_404(Tag, slug=tag_slug)
        paginator = Paginator(Post.objects.all().filter(
            tags__in=[tag]).order_by('-hit_count_generic__hits'), 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        most_view = Post.objects.order_by('-hit_count_generic__hits')[:5]
        cat = Category.objects.all()[:6]
        return render(request, 'blog/blogtag.html', {'page': page, 'posts': posts, 'tag': tag, 'most_view': most_view, 'most_tags': most_used_tags, "result": True, 'category': cat})
    except:
        return render(request, 'blog/blogtag.html', {"result": False, "tag": tag_slug})


class ArticleDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/blogsingle.html'
    count_hit = True

    def get_queryset(self):
        self.is_like = get_object_or_404(Post, id=self.kwargs['pk'])
        self.is_like = self.is_like.likes.filter(
            id=self.request.user.id).exists()
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        blog_connector = PostAPI()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        get_all_tags = context['post'].tags.all()
        context['similar_post'] = blog_connector.get_similar_post(get_all_tags,self.kwargs.get('pk'))
        context['is_liked'] = self.is_like
        context['category'] = blog_connector.get_category()
        return context


def account_redirect(request):
    if request.method == "GET":
        pk_value = int(request.GET.get("blog-redirect-id"))
        return HttpResponse("<h1>{}</h1>".format(pk_value))
    else:
        return HttpResponse("heloo")



def category_sys(request, category_slug):
    most_used_tags = Post.tags.most_common()[:6]
    try:
        paginator = Paginator(Post.objects.filter(category__name=category_slug).order_by('-hit_count_generic__hits','-date_published'), 5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        most_view = Post.objects.order_by('-date_published')[:5]
        category_name = Category.objects.all()[:6]
        return render(request, 'blog/category.html', {'page': page, 'posts': posts,'most_view': most_view, 'most_tags': most_used_tags, "result": True,"cat":category_slug,"category_name":category_name})
    except:
        return render(request, 'blog/category.html', {"result": False, "cat": category_slug})