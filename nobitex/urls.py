from django.urls import path

from nobitex.views import hello_world
from nobitex.views import trade_table

urlpatterns = [
    path('', hello_world),
    # path('/trades', trade_table)
]
