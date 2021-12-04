from typing import List
from .models import Post
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
from hitcount.views import HitCountDetailView
from django.http import JsonResponse
from api.Blog.BlogManager import PostAPI
# Create your views here.


class HomeView(ListView):

    blog_connector = PostAPI()

    model = blog_connector.post_instance
    template_name = "blog/index.html"
    ordering = ['-date_published', '-hit_count_generic__hits']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['editor'] = self.blog_connector.get_editor_post()
        context['most_used_tag'] = self.blog_connector.get_most_tags_used()
        context['trending_post'] = self.blog_connector.get_most_viewed()
        context['this_month'] = self.blog_connector.get_this_month()
        context['most_like'] = self.blog_connector.get_most_liked_post()
        context['category'] = self.blog_connector.get_category()
        return context

class PostByTags(ListView):

    blog_connector = PostAPI()

    def get_queryset(self):
        self.model = self.blog_connector.post_instance
        self.template_name = 'blog/blogtag.html'
        self.tag_slug = self.kwargs['tag_slug']
        self.paginate_by = 5
        self.ordering = ['-hit_count_generic__hits','-likes_count','-date_published'] 
        queryset = self.blog_connector.get_PostByTags_model(Tag,tag_slug=self.tag_slug)
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

    blog_connector = PostAPI()

    model = blog_connector.post_instance
    template_name = 'blog/blogsingle.html'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        get_all_tags = context['post'].tags.all()
        context['similar_post'] = self.blog_connector.get_similar_post(get_all_tags,self.kwargs.get('pk'))
        context['is_liked'] = self.blog_connector.is_post_like(self.blog_connector.post_instance,self.kwargs['pk'],self.request.user.id)
        context['category'] = self.blog_connector.get_category()
        context['category_post'] = self.blog_connector.get_PostByCategory(context['post'].category).exclude(pk=context['post'].pk)[:3]
        return context

class PostByCategory(ListView):

    blog_connector = PostAPI()

    def get_queryset(self):
        self.model = self.blog_connector.post_instance
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
        
class SearchView(ListView):
    
    blog_connector = PostAPI()

    def get_queryset(self):
        self.model = self.blog_connector.post_instance
        self.template_name = 'blog/search.html'
        self.paginate_by = 5 
        self.query = self.request.GET.get('search_query')
        queryset = self.blog_connector.search(self.query)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['most_like'] = self.blog_connector.get_most_liked_post()
        context['most_tags'] = self.blog_connector.get_most_tags_used()
        context['category'] = self.blog_connector.get_category()
        context['query'] = self.query
        return context
    
def search_sys(request):
    if request.method == "GET":
        blog_connector = PostAPI()
        query = request.GET.get('search_query')
        posts = blog_connector.search(query)
        most_like_post = blog_connector.get_most_liked_post()
        category = blog_connector.get_category() 
        return render(request, 'blog/search.html', {'query': query, 'result': posts, 'most_liked': most_like_post, 'category': category})



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
        return redirect("/blog/")
