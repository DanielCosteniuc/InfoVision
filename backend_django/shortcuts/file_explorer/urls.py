# file_explorer/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('partitions/', views.list_partitions, name='list_partitions'),
    path('list/', views.list_files, name='list_files'),
    path('download/', views.download_file, name='download_file'),
    path('server-action/', views.server_action, name='server_action'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
