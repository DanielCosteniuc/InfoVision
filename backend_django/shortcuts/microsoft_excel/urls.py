# excel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('open-excel/', views.open_excel, name='open_excel'),
    path('add-sheet/', views.add_sheet, name='add_sheet'),
    path('next-sheet/', views.next_sheet, name='next_sheet'),
    path('prev-sheet/', views.prev_sheet, name='prev_sheet'),
    path('delete-active-sheet/', views.delete_active_sheet, name='delete_active_sheet'),
    path('save-excel/', views.save_excel, name='save_excel'),
    path('activate-excel/', views.activate_excel, name='activate_excel'),
    path('close-excel/', views.close_excel_window, name='close_excel_window'),
    path('scroll-up/', views.scroll_up, name='scroll_up'),  
    path('scroll-down/', views.scroll_down, name='scroll_down'),  
    path('scroll-left/', views.scroll_left, name='scroll_left'),
    path('scroll-right/', views.scroll_right, name='scroll_right'),
    path('list_open_excel_files/', views.list_open_excel_files, name='list_open_excel_files'),
    path('activate_excel_file/', views.activate_excel_file, name='activate_excel_file'),
]
