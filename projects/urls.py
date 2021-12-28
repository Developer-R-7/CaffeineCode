from django.urls import path
from . import views
app_name = "projects"

urlpatterns = [
    path('',views.index, name="index"),
    path('github-showcase/profile/<str:username>',views.profile,name="profile"),
    path('github-showcase/profile/add',views.profile_add,name="add"),
]
