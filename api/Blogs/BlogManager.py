import datetime
from blog.models import Category,Post
from django.db.models import Count,Q
from django.shortcuts import get_object_or_404

class PostAPI():

    def __init__(self):
        self.blog_post =  Post.objects.all()
        self.post_instance = Post

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

    def get_PostByTags_model(self,Tag,tag_slug):
        try:
            tag = get_object_or_404(Tag, slug=tag_slug) 
            return self.blog_post.filter(tags__in=[tag]).order_by('-hit_count_generic__hits')
        except:
            raise Exception(" PostBy TAGS ERROR")
    def get_PostByCategory(self,category_slug):
        try:
            return self.blog_post.filter(category__name=category_slug).order_by('-hit_count_generic__hits','-likes_count','-date_published')
        except:
            raise Exception("Error in postby catgroy")
    
    def search(self,query_set):
        if query_set['search_body'] and query_set['search_title']:
            return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')
        elif query_set['search_body']:
            return self.blog_post.filter(category=query_set['category_text']).order_by('-modified').filter(Q(body__icontains=query_set['query']))
        elif query_set['search_title']:
            return self.blog_post.filter(category__name=query_set['category_text']).order_by('-modified').filter(Q(title__icontains=query_set['query']))
        else:
            return self.blog_post.filter(Q(title__icontains=query_set['query']) | Q(body__icontains=query_set['query']) | Q(blog_snipet__icontains=query_set['query'])).order_by('-modified')

    
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