from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from hitcount.models import HitCount
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    blog_snipet = models.CharField(max_length=400)
    title_tag = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(null=True, blank=True)
    date_published = models.DateField(auto_now_add=True)
    entry_img = models.URLField()
    tags = TaggableManager()
    modified = models.DateTimeField(auto_now=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    author_conculsion = models.CharField(
        max_length=300, default="No Author Review")
    readtime_min = models.IntegerField(default=0)
    editor_choice = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, default=None, blank=True, related_name='post_likes')
    likes_count = models.BigIntegerField(default='0')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})
