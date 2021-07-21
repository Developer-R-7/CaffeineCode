from django.core import paginator
from .models import Post
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from taggit.models import Tag
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q
from hitcount.views import HitCountDetailView
# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = ['-hit_count_generic__hits','-date_published']
    paginate_by = 5
    def get_context_data(self,**kwargs):
        most_used_tags = Post.tags.most_common()[:6]
        context = super(HomeView,self).get_context_data(**kwargs)
        context['most_used_tag'] = most_used_tags
        context['trending_post'] = Post.objects.order_by('-hit_count_generic__hits')[:5]
        return context

def search_sys(request):
    if request.method == "GET":
        query = request.GET.get('search_query')
        posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        posts = posts.order_by('-modified')
        return render(request,'blog/search.html',{'query':query,'result':posts})

def post_by_tags(request,tag_slug):
    most_used_tags = Post.tags.most_common()[:6]
    tag = get_object_or_404(Tag, slug=tag_slug)
    paginator = Paginator(Post.objects.all().filter(tags__in=[tag]).order_by('-hit_count_generic__hits'), 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    most_view = Post.objects.order_by('-date_published')[:5]
    return render(request, 'blog/blogtag.html', {'page': page,'posts': posts,'tag': tag,'most_view':most_view,'most_tags':most_used_tags})



class ArticleDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/blogsingle.html'
    count_hit = True
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        get_all_tags = context['post'].tags.all()
        similar_posts = Post.objects.filter(tags__in = get_all_tags).exclude(id=self.kwargs.get('pk'))
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-tags')[:5]
        context['similar_post'] = similar_posts
        return context

    