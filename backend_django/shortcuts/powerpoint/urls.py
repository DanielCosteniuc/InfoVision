from django.urls import path
from . import views

urlpatterns = [
    path('open-powerpoint/', views.open_powerpoint, name='open_powerpoint'),
    path('add-slide/', views.add_slide, name='add_slide'),
    path('save-presentation/', views.save_presentation, name='save_presentation'),
    path('delete-slide/', views.delete_slide, name='delete_slide'),
    path('start-presentation/', views.start_presentation, name='start_presentation'),
    path('next-slide/', views.next_slide, name='next_slide'),
    path('previous-slide/', views.previous_slide, name='previous_slide'),
    path('increase-volume/', views.increase_volume, name='increase_volume'),
    path('decrease-volume/', views.decrease_volume, name='decrease_volume'),
    path('stop-presentation/', views.stop_presentation, name='stop_presentation'),
    path('go-to-first-slide/', views.go_to_first_slide, name='go_to_first_slide'),
    path('go-to-last-slide/', views.go_to_last_slide, name='go_to_last_slide'),
    path('activate-powerpoint/', views.activate_powerpoint, name='activate_powerpoint'),
    path('close-powerpoint/', views.close_powerpoint, name='close_powerpoint'),
     path('list_open_powerpoint_files/', views.list_open_powerpoint_files, name='list_open_powerpoint_files'),
    path('activate_powerpoint_file/', views.activate_powerpoint_file, name='activate_powerpoint_file'),
]
