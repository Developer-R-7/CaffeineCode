from django.core import paginator
from .models import Post
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = ['-date_published']
    paginate_by = 3

def search_sys(request):
    if request.method == "GET":
        query = request.GET.get('search_query')
        paginator = Paginator(Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)),9)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request,'blog/search.html',{'page':page,'query':query,'result':posts})

def post_by_tags(request,tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    paginator = Paginator(Post.objects.all().filter(tags__in=[tag]), 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/blogtag.html', {'page': page,'posts': posts,'tag': tag})

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'blog/blogsingle.html'
    
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        #Adding similar posts in blogsingle
        get_all_tags = context['post'].tags.all()
        similar_posts = Post.objects.filter(tags__in = get_all_tags).exclude(id=self.kwargs.get('pk'))
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]
        context['similar_post'] = similar_posts
        return context

    