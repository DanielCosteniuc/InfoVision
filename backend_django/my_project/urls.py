#/my_project/urls.py
from django.contrib import admin
from django.urls import path, include
from shortcuts import views as shortcuts_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('shortcuts/', include('shortcuts.urls')),
    path('api/server-info/', shortcuts_views.server_info, name='server-info'),
    
]
