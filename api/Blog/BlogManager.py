import datetime
from blog.models import Category,Post
from django.db.models import Count
from django.shortcuts import get_object_or_404

class PostAPI():

    def __init__(self):
        self.blog_post =  Post.objects.all()

    def get_category(self):
        category = Category.objects.all()[:6]
        return category
    
    def get_similar_post(self,tags,id):
        try :
            return self.blog_post.filter(tags__in=tags).exclude(id=id).annotate(same_tags=Count('tags')).order_by('-tags')[:5]
        except:
            raise Exception("Failed 'get_similar_post'")
    
    def get_editor_post(self):
        try:
            return self.blog_post.filter(editor_choice=True).order_by('-hit_count_generic__hits')[:5]
        except:
            raise Exception("Failed 'get_editor_post'")

    def get_most_tags_used(self):
        try:
            return Post.tags.most_common()[:10]
        except:
            raise Exception("Failed 'get_most_tags_used'")
    
    def get_most_liked_post(self):
        try:
            return self.blog_post.order_by('-likes_count','-hit_count_generic__hits')[:5]
        except:
            raise Exception("Failed 'get_most_liked_post'")

    def get_this_month(self):
        try:
            get_date = datetime.date.today()
            return self.blog_post.filter(date_published__year=get_date.year, date_published__month=get_date.month).order_by('-hit_count_generic__hits')[:10]
        except:
            raise Exception("Failed 'get_this_month'")

    def get_most_viewed(self):
        try:
            return self.blog_post.order_by('-hit_count_generic__hits')[:5]
        except:
            raise Exception("Failed 'get_most_view'")

    def search_blog(self):
        pass

    def is_post_like(self,post,id,user_id):
        try:
            return get_object_or_404(post, id=id).likes.filter(id=user_id).exists()
        except:
            return None

    
    def get_post_tags(self,tag,tag_slug):
        try:
            return get_object_or_404(tag,slug=tag_slug)
        except:
            return None

    def get_PostByTags_model(self,tag):
        #try:
        return self.blog_post.filter(tags__in=[tag]).order_by('-hit_count_generic__hits')
        #except:
            #raise Exception(" PostBy TAGS ERROR") 