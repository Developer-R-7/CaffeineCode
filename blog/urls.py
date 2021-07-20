from django.urls import path
from .views import HomeView,ArticleDetailView
from . import views
app_name = "blog"
urlpatterns = [
    #path('blog/',views.blog_index,name="blogIndex")
    path('',HomeView.as_view(),name="index"),
    path('article/<int:pk>',ArticleDetailView.as_view(),name="blog_details"),
    path('tag/<tag_slug>', views.post_by_tags, name='post_list_by_tags'),
    path('search/',views.search_sys,name='search_qu'),
]