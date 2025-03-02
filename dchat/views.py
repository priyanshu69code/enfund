from django.shortcuts import render, get_object_or_404
from .models import ChatGroup

def chat_room(request, group_name):
    group = get_object_or_404(ChatGroup, name=group_name)
    return render(request, 'chat/room.html', {'group_name': group.name})
