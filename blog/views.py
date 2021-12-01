from .models import Post, Category
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
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

class PostByTags(ListView):
    def get_queryset(self):
        self.blog_connector = PostAPI()
        self.model = Post
        self.template_name = 'blog/blogtag.html'
        self.tag_slug = self.kwargs['tag_slug']
        self.paginate_by = 5
        self.ordering = ['-hit_count_generic__hits','-likes_count','-date_published']
        self.tag = get_object_or_404(Tag, slug=self.tag_slug)   
        queryset = self.blog_connector.get_PostByTags_model(self.tag)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(PostByTags, self).get_context_data(**kwargs)
        context['most_view'] = self.blog_connector.get_most_viewed()
        context['most_tags'] = self.blog_connector.get_most_tags_used()
        context['category'] = self.blog_connector.get_category()
        context['result'] = True
        context['tag'] = self.tag_slug
        return context

class ArticleDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/blogsingle.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        blog_connector = PostAPI()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        get_all_tags = context['post'].tags.all()
        context['similar_post'] = blog_connector.get_similar_post(get_all_tags,self.kwargs.get('pk'))
        context['is_liked'] = blog_connector.is_post_like(Post,self.kwargs['pk'],self.request.user.id)
        context['category'] = blog_connector.get_category()
        return context

class PostByCategory(ListView):

    def get_queryset(self):
        self.blog_connector = PostAPI()
        self.model = Post
        self.template_name = 'blog/category.html'
        self.category_slug = self.kwargs['category_slug']
        self.paginate_by = 5 
        queryset = self.blog_connector.get_PostByCategory(self.category_slug)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(PostByCategory, self).get_context_data(**kwargs)
        context['most_view'] = self.blog_connector.get_most_viewed()
        context['most_tags'] = self.blog_connector.get_most_tags_used()
        context['category'] = self.blog_connector.get_category()
        context['cat'] = self.category_slug
        context['result'] = True
        return context
        

    
def search_sys(request):
    if request.method == "GET":
        query = request.GET.get('search_query')
        posts = Post.objects.filter(Q(title__icontains=query) | Q(
            body__icontains=query) | Q(blog_snipet__icontains=query)).order_by('-modified')
        most_like_post = Post.objects.all().order_by('-likes_count')[:5]
        cat = Category.objects.all()[:6]
        return render(request, 'blog/search.html', {'query': query, 'result': posts, 'most_liked': most_like_post, 'category': cat})


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
