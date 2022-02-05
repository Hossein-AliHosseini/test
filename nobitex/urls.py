from django.urls import path

from nobitex.views import hello_world

urlpatterns = [
    path('', hello_world),
]