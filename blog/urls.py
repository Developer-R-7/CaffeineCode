from typing import List
from django.urls import path
from .views import HomeView, ArticleDetailView, like_sys,ListView
from . import views
app_name = "blog"
urlpatterns = [
    # path('blog/',views.blog_index,name="blogIndex")
    path('', HomeView.as_view(), name="index"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name="blog_details"),
    path('like/', like_sys, name="like"),
    path('tag/<tag_slug>', views.post_by_tags, name='post_list_by_tags'),
    path('search/', views.search_sys, name='search_qu'),
    path('subcribe-newsletter/', views.newsletter, name="newsletter"),
    path('account-redirect/', views.account_redirect, name="account_redirect"),
    path('category/<category_slug>',views.category_sys,name="category"),
]
