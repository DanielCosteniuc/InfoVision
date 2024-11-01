from django.urls import path
from . import views

urlpatterns = [
    path('oauth/login/', views.zoom_login, name='zoom_login'),
    path('oauth/callback/', views.zoom_oauth_callback, name='zoom_oauth_callback'),
    path('get-contacts/', views.get_zoom_chat_contacts, name='get_zoom_chat_contacts'),
    path('open-zoom/', views.open_zoom, name='open_zoom'),
    #path('close-zoom/', views.close_zoom, name='close_zoom'),
    path('check-auth/', views.check_auth, name='check_auth'),
]
