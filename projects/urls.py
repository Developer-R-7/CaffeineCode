from django.urls import path
from . import views
app_name = "projects"

urlpatterns = [
    path(r'',views.index, name="index")
]
