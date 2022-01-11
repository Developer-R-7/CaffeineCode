from django.urls import path
from . import views

app_name = 'config'


urlpatterns = [
    path(r'maintenance/', views.maintenance, name='maintenance'),
]