"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path ,include
from django.conf.urls import handler500,handler404

urlpatterns = [
    path(r'',include('IndexHome.urls')),
    path(r'admin/', admin.site.urls),
    path(r'blog/',include('blog.urls')),
    path(r'hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path(r'api-auth/', include('rest_framework.urls')),
    path(r'projects/',include("projects.urls")),
    path(r'config/',include("Config.urls")),

]
handler500 = "Config.views.handler500"
handler404 = "Config.views.handler404"

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
