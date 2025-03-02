from django.urls import path
from .views import chat_room

urlpatterns = [
    path('chat/<str:group_name>/', chat_room, name='chat_room'),
]
