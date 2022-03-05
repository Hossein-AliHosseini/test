from django.urls import path
from index.views import MA_view, EMA_view, SO_view, ADI_view, check_index_status

urlpatterns = [
    path('ma', MA_view, name='ma'),
    path('ema', EMA_view, name='ema'),
    path('so', SO_view, name='so'),
    path('adi', ADI_view, name='adi'),
    path('check_index_status', check_index_status, name='check_index_status')
]
