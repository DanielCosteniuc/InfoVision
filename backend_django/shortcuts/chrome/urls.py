# chrome/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('open-chrome/', views.open_chrome, name='open_chrome'),
    path('activate-chrome/', views.activate_chrome, name='activate_chrome'),
    path('close-current-tab/', views.close_current_tab, name='close_current_tab'),
    path('next-tab/', views.next_tab, name='next_tab'),
    path('previous-tab/', views.previous_tab, name='previous_tab'),
    path('open-gmail/', views.open_gmail, name='open_gmail'),
    path('open-youtube/', views.open_youtube, name='open_youtube'),
    path('open-chrome-new-tab/', views.open_chrome_new_tab, name='open_chrome_new_tab'),
    path('open-drive/', views.open_drive, name='open_drive'),
    path('open-calendar/', views.open_calendar, name='open_calendar'),
    path('scroll-down-chrome/', views.scroll_down_chrome, name='scroll_down_chrome'),
    path('scroll-up-chrome/', views.scroll_up_chrome, name='scroll_up_chrome'),
]
