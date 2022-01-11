from django.shortcuts import redirect
from django.views.generic import ListView
from taggit.models import Tag
from hitcount.views import HitCountDetailView
from django.http import JsonResponse
from connectors.Blogs.BlogManager import PostConnector



class HomeView(ListView):

    blog_connector = PostConnector()

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
        context['redirect_url'] = self.request.get_full_path()
        return context

class PostByTags(ListView):

    blog_connector = PostConnector()

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

    blog_connector = PostConnector()

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
        context['redirect_url'] = self.request.get_full_path()
        return context

class PostByCategory(ListView):

    blog_connector = PostConnector()

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
    
    blog_connector = PostConnector()

    def get_queryset(self):
        self.model = self.blog_connector.post_instance
        self.template_name = 'blog/search.html'
        self.paginate_by = 5 
        self.query = self.request.GET.get('query')

        # Getting Query Data
        try:
            self.search_title = self.request.GET.get('search_title')
        except:
            pass
        try:
            self.search_body =self.request.GET.get('search_body')
        except:
            pass
        try:
            self.category_search = self.request.GET.get('category_selected')
        except:
            pass
        
        # Data Cleaning Functions
        def query_none_checker(query_params):
            if query_params is None:
                return False
            else:
                return True
        def category_parser(number):
            category_list = ["uncategorized","education","creative","data-structures","projects","algorithms"]
            if number != "None":
                return category_list[int(number)]
            else:
                return None

        # Final Query Set
        self.search_query_set = {
            'query':self.query,
            'search_body':query_none_checker(self.search_body),
            'search_title':query_none_checker(self.search_title),
            'category_text':category_parser(self.category_search)
        }
        queryset = self.blog_connector.search(self.search_query_set)
        return queryset

    def get_context_data(self,**kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['most_like'] = self.blog_connector.get_most_liked_post()
        context['most_tags'] = self.blog_connector.get_most_tags_used()
        context['category'] = self.blog_connector.get_category()
        context['query_set'] = self.search_query_set
        context['post'] = self.blog_connector.get_recent_post()
        return context
    
def like_sys(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method == "POST":
            blog_connector = PostConnector()
            result = ''
            pk_value = int(request.POST.get("postid"))
            post = blog_connector.like(pk_value,request)
            return JsonResponse({"result": post})
    else:
        return redirect("/blog/")
