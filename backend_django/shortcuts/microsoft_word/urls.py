# word/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('open-word/', views.open_word, name='open_word'),
    path('go-to-end/', views.go_to_end, name='go_to_end'),
    path('go-to-start/', views.go_to_start, name='go_to_start'),
    path('page-down/', views.page_down, name='page_down'),
    path('page-up/', views.page_up, name='page_up'),
    path('save-as/', views.save_as, name='save_as'),
    path('activate-word/', views.activate_word, name='activate_word'),
    path('zoom-in/', views.zoom_in, name='zoom_in'),
    path('zoom-out/', views.zoom_out, name='zoom_out'),
    path('read-mode/', views.read_mode, name='read_mode'),
    path('read-mode-next-page/', views.read_mode_next_page, name='read_mode_next_page'),
    path('read-mode-previous-page/', views.read_mode_previous_page, name='read_mode_previous_page'),
    path('exit-read-mode/', views.exit_read_mode, name='exit_read_mode'),
    path('close-word/', views.close_word, name='close_word'),
    path('list_open_word_files/', views.list_open_word_files, name='list_open_word_files'),
    path('activate_word_file/', views.activate_word_file, name='activate_word_file'),
    
]
