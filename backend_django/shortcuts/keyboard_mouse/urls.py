from django.urls import path
from . import views

urlpatterns = [
    path('move_mouse/', views.move_mouse_view, name='move_mouse'),
    path('keyboard_input/', views.keyboard_input_view, name='keyboard_input'),  # Endpoint pentru textul tastat
]
