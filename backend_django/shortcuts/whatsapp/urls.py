from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path('open-whatsapp/', views.open_whatsapp, name='open_whatsapp'),
    path('activate-whatsapp/', views.activate_whatsapp, name='activate_whatsapp'),
    path('capture-qr-whatsapp/', views.capture_qr_whatsapp, name='capture_qr_whatsapp'),
    path('next-chat/', views.next_chat, name='next_chat'),
    path('previous-chat/', views.previous_chat, name='previous_chat'),
    path('open-chat/', views.open_chat, name='open_chat'),  
    path('close-chat/', views.close_chat, name='close_chat'),  
    path('start-audio-call/', views.start_audio_call, name='start_audio_call'),  
    path('start-video-call/', views.start_video_call, name='close_chat'),  
    path('close-call/', views.close_call, name='close_call'),
    path('logout-whatsapp/', views.logout_whatsapp, name='logout_whatsapp'),
    path('close-whatsapp/', views.close_whatsapp, name='close_whatsapp'),
] + static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
