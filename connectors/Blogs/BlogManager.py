import datetime
from blog.models import Category,Post
from django.db.models import Count,Q
from django.shortcuts import get_object_or_404
from ..Cache.CacheManager import cache_manager
TIME = 300
class PostConnector():

    def __init__(self):
        self.blog_post =  Post.objects.all()
        self.post_instance = Post

    def get_category(self):
        category = Category.objects.all()[:6]
        return cache_manager('get_category',category,TIME)
    
    def get_similar_post(self,tags,id):
        try :
            return cache_manager('similar_post',self.blog_post.filter(tags__in=tags).exclude(id=id).annotate(same_tags=Count('tags')).order_by('-tags')[:5],TIME)
        except:
            raise Exception("Failed (get_similar_post)")
    
    def get_editor_post(self):
        try:
            return cache_manager('editor_post',self.blog_post.filter(editor_choice=True).order_by('-hit_count_generic__hits')[:5],TIME)
        except:
            raise Exception("Failed (get_editor_post)")

    def get_most_tags_used(self):
        try:
            return cache_manager('most_tags_used',Post.tags.most_common()[:10],TIME)
        except:
            raise Exception("Failed (get_most_tags_used)")
    
    def get_most_liked_post(self):
        try:
            return cache_manager('mst_liked_post',self.blog_post.order_by('-likes_count','-hit_count_generic__hits')[:5],TIME)
        except:
            raise Exception("Failed (get_most_liked_post)")

    def get_this_month(self):
        try:
            get_date = datetime.date.today()
            return cache_manager('this_month_post',self.blog_post.filter(date_published__year=get_date.year, date_published__month=get_date.month).order_by('-hit_count_generic__hits')[:10],TIME)
        except:
            raise Exception("Failed (get_this_month)")

    def get_most_viewed(self):
        try:
            return cache_manager('most_viewed',self.blog_post.order_by('-hit_count_generic__hits')[:5],TIME)
        except:
            raise Exception("Failed (get_most_viewed)'")

    def is_post_like(self,post,id,user_id):    
        return get_object_or_404(post, id=id).likes.filter(id=user_id).exists()

    def get_post_tags(self,tag,tag_slug):
        return get_object_or_404(tag,slug=tag_slug)

    def get_PostByTags_model(self,Tag,tag_slug):
        try:
            tag = get_object_or_404(Tag, slug=tag_slug) 
            return cache_manager('post_by_tags',self.blog_post.filter(tags__in=[tag]).order_by('-hit_count_generic__hits'),TIME)
        except:
            raise Exception("Failed (get_PostByTags_model)")
    
    def get_PostByCategory(self,category_slug):
        try:
            return cache_manager('post_by_category',self.blog_post.filter(category__name=category_slug).order_by('-hit_count_generic__hits','-likes_count','-date_published'),TIME)
        except:
            raise Exception("Failed (get_PostByCategory)")
    
    def search(self,query_set):
        if query_set['category_text'] is not None:
            if query_set['search_body'] and query_set['search_title']:
                return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')
            elif query_set['search_body']:
                return self.blog_post.filter(category=query_set['category_text']).order_by('-modified').filter(Q(body__icontains=query_set['query']))
            elif query_set['search_title']:
                return self.blog_post.filter(category__name=query_set['category_text']).order_by('-modified').filter(Q(title__icontains=query_set['query']))
            else:
                return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')
        else:
            if query_set['search_body'] and query_set['search_title']:
                return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')
            elif query_set['search_body']:
                return self.blog_post.filter(Q(body__icontains=query_set['query'])).order_by('-modified')
            elif query_set['search_title']:
                return self.blog_post.filter(Q(title__icontains=query_set['query'])).order_by('-modified')
            else:
                return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')

    def get_recent_post(self):
        try:
            return cache_manager('recent_post',self.blog_post.order_by('-likes_count','-date_published')[:3],TIME)
        except:
            raise Exception("Failed (get_recent_post)")

    def like(self,pk,request):
        post = get_object_or_404(self.post_instance, id=pk)
        result = ''
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
        return result