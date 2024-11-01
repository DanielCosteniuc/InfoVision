from . import views
from django.urls import path

urlpatterns = [
    path('open-skype/', views.open_skype, name='open_skype'),
    path('close-skype/', views.close_skype, name='close_skype'),
    path('open-chats/', views.open_chats, name='open_chats'),
    path('open-contacts/', views.open_contacts, name='open_contacts'),
    path('next-conversation/', views.next_conversation, name='next_conversation'),
    path('previous-conversation/', views.previous_conversation, name='previous_conversation'),
    path('start-video-call/', views.start_video_call, name='start_video_call'),
    path('start-audio-call/', views.start_audio_call, name='start_audio_call'),
    path('toggle-mute/', views.toggle_mute, name='toggle_mute'),
    path('toggle-camera/', views.toggle_camera, name='toggle_camera'),
    path('add-people-to-call/', views.add_people_to_call, name='add_people_to_call'),
    path('navigate-up/', views.navigate_up, name='navigate_up'),
    path('navigate-down/', views.navigate_down, name='navigate_down'),
    path('hang-up/', views.hang_up, name='hang_up'),
    path('answer-call/', views.answer_call, name='answer_call'),
    path('open-contact/', views.open_contact, name='open_contact'),
]
