from django.urls import path

from nobitex.views import view_trades, hello_world, candlestick_charts

urlpatterns = [
    path('', hello_world),
    path('trades', view_trades),
    path('charts', candlestick_charts),
]
