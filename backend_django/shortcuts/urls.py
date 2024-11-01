#/shortcuts/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('api/server-info/', views.server_info, name='server-info'),
    path('teams/', include('shortcuts.microsoft_teams.urls')),  
    path('word/', include('shortcuts.microsoft_word.urls')),
    path('excel/', include('shortcuts.microsoft_excel.urls')),
    path('powerpoint/', include('shortcuts.powerpoint.urls')),
    path('pdf/', include('shortcuts.pdf.urls')),
    path('chrome/', include('shortcuts.chrome.urls')),
    path('file-explorer/', include('shortcuts.file_explorer.urls')),
    path('zoom/', include('shortcuts.zoom.urls')),
    path('whatsapp/', include('shortcuts.whatsapp.urls')),
    path('skype/', include('shortcuts.skype.urls')),
    path('keyboard_mouse/', include('shortcuts.keyboard_mouse.urls')),
]

