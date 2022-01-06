from django.urls import path
from . import views
app_name = "projects"

urlpatterns = [
    path(r'',views.index, name="index"),
    path(r'github-showcase/',views.githubShowcase,name="githubShowcase"),
    path(r'github-showcase/profile/<str:username>',views.profile,name="profile"),
    path(r'github-showcase/profile-add/',views.profile_add,name="add"),
]
