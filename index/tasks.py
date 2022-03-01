from datetime import timedelta, datetime

from celery import shared_task

from django.db.models import Avg, Max, Min

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
                                     market=Market.objects.get(id=market_id)).\
                                         aggregate(moving_average=Avg('price'))
    new_ma = MA.objects.create(start=start,
                               end=end,
                               volume=float(queryset['moving_average']))
    return new_ma.volume


@shared_task
def ema(start, end, market_id, duration):
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    end = datetime.strptime(str(end)[:10], '%Y-%m-%d')
    cache = EMA.objects.filter(start=start, end=end).first()
    if cache:
        return cache.volume
    multiplier = 2 / (1 + duration)
    market = Market.objects.get(id=market_id)
    first = Trades.objects.filter(market=market).order_by('time').first()
    queryset = Trades.objects.filter(time__date__gte=start,
                                     time__date__lte=end,
                                     market=market)
    if start == first.time.date():
        queryset = queryset.aggregate(moving_average=Avg('price'))
        new_ema = EMA.objects.create(start=start,
                                     end=end,
                                     volume=float(queryset['moving_average']))
        return new_ema.volume
    else:
        close_price = queryset.order_by('time').last().price
        volume = close_price * multiplier +\
            ema(start-timedelta(days=1),
                end-timedelta(days=1),
                market_id, duration) * (1 - multiplier)
        new_ema = EMA.objects.create(start=start, end=end, volume=volume)
        return volume


@shared_task
def so(start, market_id):
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    cache = SO.objects.filter(start=start).first()
    if cache:
        return cache.volume
    market = Market.objects.get(id=market_id)
    close_price = Trades.objects.filter(time__date__gte=start-timedelta(days=14),
                                          time__date__lte=start,
                                          market=market).\
                                              order_by('time').last().price
    queryset = Trades.objects.filter(time__date__gte=start,
                                     time__date__lte=start+timedelta(days=14),
                                     market=market).\
                                         aggregate(low=Min('price'),
                                                   high=Max('price'))
    K = (close_price - queryset['low']) / (queryset['high'] - queryset['low'])
    new_so = SO.objects.create(start=start, volume=K)
    return new_so.volume


@shared_task
def adi(start, end, market_id):
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    end = datetime.strptime(str(end)[:10], '%Y-%m-%d')
    cache = ADI.objects.filter(start=start, end=end).first()
    if cache:
        return cache.volume
    market = Market.objects.get(id=market_id)
    queryset = Trades.objects.filter(time__date__gte=start,
                                     time__date__lte=end,
                                     market=market).\
                                         aggregate(low=Min('price'),
                                                   high=Max('price'))
    close = Trades.objects.filter(time__date__gte=start,
                                  time__date__lte=end,
                                  market=market).order_by('time').last().price
    MFM = ((close - queryset['low']) - (queryset['high'] - close)) /\
        (queryset['high'] - queryset['low'])
    if start == Trades.objects.filter(market=market).order_by('time').first().time.date():
        new_adi = ADI.objects.create(start=start, end=end, volume=MFM)
        return new_adi.volume
    else:
        perv_adi = adi(start-timedelta(days=1),
                       end-timedelta(days=1),
                       market_id)
        new_adi = ADI.objects.create(start=start, end=end, volume=MFM+perv_adi)
        return new_adi.volume
