from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from chat.models import Message


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    email = request.GET.get('email', 'Anonymous')
    messages = Message.objects.filter(room=room_name)

    return render(request, 'room.html', {'room_name': room_name,
                                         'email': email,
                                         'messages': messages})
