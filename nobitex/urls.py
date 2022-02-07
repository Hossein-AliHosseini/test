from django.urls import path

from nobitex.views import view_trades, hello_world

urlpatterns = [
    path('', hello_world),
    path('trades', view_trades),
]
