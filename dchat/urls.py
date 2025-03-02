from django.urls import path
from .views import chat_room

app_name = 'dchat'

urlpatterns = [
    path('chat/<str:group_name>/', chat_room, name='chat_room'),
]
