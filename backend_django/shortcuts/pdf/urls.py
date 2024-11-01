# pdf/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('open-acrobat/', views.open_acrobat, name='open_acrobat'),
    path('activate-acrobat/', views.activate_acrobat, name='activate_acrobat'),
    path('next-page-pdf/', views.next_page, name='next_page_pdf'),
    path('previous-page-pdf/', views.previous_page, name='previous_page_pdf'),
    path('zoom-in-pdf/', views.zoom_in, name='zoom_in_pdf'),
    path('zoom-out-pdf/', views.zoom_out, name='zoom_out_pdf'),
    path('read-mode-pdf/', views.read_mode, name='read_mode_pdf'),
    path('print-pdf/', views.print_pdf, name='print_pdf'),
    path('close-acrobat/', views.close_acrobat, name='close_acrobat'),
]
