from celery import shared_task

from django.db.models import Avg

from nobitex.models import Trades, Market
from .models import *
# save data after calculation


@shared_task
def ma(start, end, market_id):
    cache = MA.objects.filter(start=start, end=end).first()
    if cache:
        return cache.volume
    queryset = Trades.objects.filter(time__date__gte=start,
                                     time__date__lte=end,
                                     market=Market.objects.get(id=market_id)).aggregate(moving_average=Avg('price'))
    new_ma = MA.objects.create(start=start,
                               end=end,
                               volume=float(queryset['moving_average']))
    return new_ma.volume


@shared_task
def ema(start, end, market_id):
    pass


@shared_task
def so(start, market_id):
    pass


@shared_task
def adi(start, end, market_id):
    pass
