from typing import List
from django.urls import path
from .views import HomeView, ArticleDetailView, like_sys, PostByTags, PostByCategory
from . import views
app_name = "blog"
urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="blog_details"),
    path('like/', like_sys, name="like"),
    path('tag/<tag_slug>', PostByTags.as_view(), name='post_list_by_tags'),
    path('search/', views.search_sys, name='search_qu'),
    path('category/<category_slug>',PostByCategory.as_view(),name="category"),
]
