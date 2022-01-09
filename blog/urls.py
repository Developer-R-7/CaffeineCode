from django.urls import path
from django.views.decorators.cache import cache_page
from .views import HomeView, ArticleDetailView, like_sys, PostByTags, PostByCategory,SearchView
app_name = "blog"
urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path(r'article/<int:pk>', ArticleDetailView.as_view(), name="blog_details"),
    path(r'like/', like_sys, name="like"),
    path(r'tag/<tag_slug>', PostByTags.as_view(), name='post_list_by_tags'),
    path(r'search/', SearchView.as_view(), name='search_qu'),
    path(r'category/<category_slug>',cache_page(1800)(PostByCategory.as_view()),name="category"),
]
