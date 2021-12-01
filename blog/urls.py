from typing import List
from django.urls import path
from .views import HomeView, ArticleDetailView, like_sys, PostByTags
from . import views
app_name = "blog"
urlpatterns = [
    # path('blog/',views.blog_index,name="blogIndex")
    path('', HomeView.as_view(), name="index"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="blog_details"),
    path('like/', like_sys, name="like"),
    path('tag/<tag_slug>', PostByTags.as_view(), name='post_list_by_tags'),
    path('search/', views.search_sys, name='search_qu'),
    path('account-redirect/', views.account_redirect, name="account_redirect"),
    path('category/<category_slug>',views.category_sys,name="category"),
]
