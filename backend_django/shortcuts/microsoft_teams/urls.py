
from django.urls import path
from . import views

urlpatterns = [
    path('open-teams/', views.open_microsoft_teams, name='open_microsoft_teams'),
    path('close-teams/', views.close_microsoft_teams, name='open_microsoft_teams'),
    path('activity/', views.navigate_activity, name='navigate_activity'),
    path('chat/', views.navigate_chat, name='navigate_chat'),
    path('teams/', views.navigate_teams, name='navigate_teams'),
    path('assignments/', views.navigate_assignments, name='navigate_assignments'),
    path('calendar/', views.navigate_calendar, name='navigate_calendar'),
    path('calls/', views.navigate_calls, name='navigate_calls'),
    path('onedrive/', views.navigate_onedrive, name='navigate_onedrive'),
    path('arrow-up/', views.arrow_up, name='arrow_up'),
    path('arrow-down/', views.arrow_down, name='arrow_down'),
    path('start-audio-call/', views.start_audio_call, name='start_audio_call'),
    path('start-video-call/', views.start_video_call, name='start_video_call'),
    path('end-call/', views.end_call, name='end_call'),
    path('mute-microphone/', views.mute_microphone, name='mute_microphone'),
    path('toggle-camera/', views.toggle_camera, name='toggle_camera'),
    path('volume-up/', views.increase_volume, name='increase_volume'),
    path('volume-down/', views.decrease_volume, name='decrease_volume'),
    path('volume-mute/', views.mute_volume, name='mute_volume'),
    path('end-call-reject/', views.reject_call, name='reject_call'),
    path('accept-audio-call/', views.accept_audio, name='accept_audio'),
    path('accept-video-call/', views.accept_video, name='accept_video'),
    path('maximize-active-window/', views.maximize_active_window, name='maximize_active_window'),

]
