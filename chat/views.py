from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

from chat.models import Message


@login_required(login_url='signup')
def index(request):
    user = request.user
    return render(request, 'index.html', {'user': user})


def room(request, room_name):
    email = request.GET.get('email', 'Anonymous')
    messages = Message.objects.filter(room=room_name)

    return render(request, 'room.html', {'room_name': room_name,
                                         'email': email,
                                         'messages': messages})
