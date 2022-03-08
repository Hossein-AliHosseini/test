from django.urls import path

from chat.views import room, index

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', room, name='room'),
]
