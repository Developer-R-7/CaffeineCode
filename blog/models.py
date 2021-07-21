from django.db import models
from django.contrib.auth.models import User
from datetime import MAXYEAR, datetime,date
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    blog_snipet = models.CharField(max_length=200)
    title_tag = models.CharField(max_length=20)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(null=True,blank=True)
    date_published = models.DateField(auto_now_add=True)
    entry_img = models.URLField(max_length=500)
    tags = TaggableManager()
    modified = models.DateTimeField(auto_now=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    author_conculsion = models.CharField(max_length=300,default="No Author Review")
    readtime_min = models.IntegerField(default=0) 
    def __str__(self):
        return self.title + '|' + str(self.author)