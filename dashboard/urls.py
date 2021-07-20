from django.urls import path
from . import views
app_name = 'dashboard_app'
urlpatterns = [
    path('dashboard/profile/<int:account_id>/',views.dashboard, name='dashboard')
]