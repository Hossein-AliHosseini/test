from django.urls import path

from nobitex.views import (view_trades, hello_world,
                           candlestick_charts, check_status)

urlpatterns = [
    path('', hello_world),
    path('trades', view_trades, name="trades"),
    path('charts', candlestick_charts, name='charts'),
    path('check_status', check_status, name='check_status'),
]
