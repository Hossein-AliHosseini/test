from datetime import timedelta, datetime

from celery import shared_task

from django.db.models import Avg, Max, Min
from django.contrib.auth import get_user_model
from django.db.models import Min, Max, DateTimeField
from django.db.models.functions import Trunc

from nobitex.models import Trade, Market
from index.models import (MA, EMA, SO, ADI,
                          MA_Base, EMA_Base, SO_Base, ADI_Base)

User = get_user_model()


@shared_task
def ma(user, start, end, market_id):
    res, temp_start, temp_end = None
    user = User.objects.get(email=user)
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    end = datetime.strptime(str(end)[:10], '%Y-%m-%d')
    market = Market.objects.get(id=market_id)
    cache = MA_Base.objects.filter(start__gte=start,
                                   end__lte=end,
                                   market=market)
    if cache.exists() and user.has_perm('index.view_ma'):
        res = MA.objects.filter(base__in=cache).order_by('period_start')
        first = res.first().period_start.date()
        last = res.last().period_start.date()
        if first == start and last == end:
            return res[:]
        temp_start = first
        temp_end = last
    if user.has_perm('index.create_ma'):
        queryset = (Trade.objects.filter(time__date__gte=start,
                                         time__date__lte=temp_start,
                                         market=market).
                    order_by('time').
                    annotate(period_start=Trunc('time', 'hour',
                                                output_field=DateTimeField())).
                    order_by('period_start').values('period_start').
                    annotate(value=Avg('price')).
                    values('period_start', 'value'))
        base_ma = MA_Base.objects.create(start=start,
                                         end=temp_start,
                                         market=market)
        for ma in queryset:
            MA.objects.create(base=base_ma,
                              period_start=ma['period_start'],
                              value=ma['value'])
        res |= queryset[:]

        queryset = (Trade.objects.filter(time__date__gte=temp_end,
                                         time__date__lte=end,
                                         market=market).
                    order_by('time').
                    annotate(period_start=Trunc('time', 'hour',
                                                output_field=DateTimeField())).
                    order_by('period_start').values('period_start').
                    annotate(value=Avg('price')).
                    values('period_start', 'value'))
        base_ma = MA_Base.objects.create(start=temp_end,
                                         end=end, market=market)
        for ma in queryset:
            MA.objects.create(base=base_ma,
                              period_start=ma['period_start'],
                              value=ma['value'])
        res |= queryset[:]

        return res
    else:
        return 'You do not have permission to access this index'


@shared_task
def ema(user, start, end, market_id, duration, first):
    user = User.objects.get(email=user)
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    end = datetime.strptime(str(end)[:10], '%Y-%m-%d')
    first = datetime.strptime(str(first)[:10], '%Y-%m-%d')
    cache = EMA.objects.filter(start=start, end=end).first()
    if cache and user.has_perm('index.view_ema'):
        return cache.volume
    multiplier = 2 / (1 + duration)
    market = Market.objects.get(id=market_id)
    queryset = Trade.objects.filter(time__date__gte=start,
                                    time__date__lte=end,
                                    market=market)
    if start == first:
        queryset = queryset.aggregate(moving_average=Avg('price'))
        if user.has_perm('index.create_ema'):
            new_ema = EMA.objects.create(start=start,
                                         end=end,
                                         volume=float(queryset['moving_average']))
            return new_ema.volume
        else:
            return 'You do not have permission to access this index'
    else:
        close_price = queryset.order_by('time').last().price
        volume = close_price * multiplier +\
            ema(start-timedelta(days=1),
                end-timedelta(days=1),
                market_id, duration, first) * (1 - multiplier)
    if user.has_perm('index.create_ema'):
        new_ema = EMA.objects.create(start=start, end=end, volume=volume)
        return new_ema.volume
    else:
        return 'You do not have permission to access this index'


@shared_task
def so(user, start, market_id):
    user = User.objects.get(email=user)
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    cache = SO.objects.filter(start=start).first()
    if cache and user.has_perm('index.create_so'):
        return cache.volume
    market = Market.objects.get(id=market_id)
    close_price = Trade.objects.filter(time__date__gte=start-timedelta(days=14),
                                       time__date__lte=start,
                                       market=market).\
                                        order_by('time').last().price
    queryset = Trade.objects.filter(time__date__gte=start-timedelta(days=14),
                                    time__date__lte=start,
                                    market=market).\
                                        aggregate(low=Min('price'),
                                                  high=Max('price'))
    K = ((close_price - queryset['low']) / (queryset['high'] - queryset['low'])) * 100
    if user.has_perm('index.create_so'):
        new_so = SO.objects.create(start=start, volume=K)
        return new_so.volume
    else:
        return 'You do not have permission to access this index'


@shared_task
def adi(user, start, end, market_id, first):
    user = User.objects.get(email=user)
    start = datetime.strptime(str(start)[:10], '%Y-%m-%d')
    end = datetime.strptime(str(end)[:10], '%Y-%m-%d')
    first = datetime.strptime(str(first)[:10], '%Y-%m-%d')
    cache = ADI.objects.filter(start=start, end=end).first()
    if cache and user.has_perm('index.view_adi'):
        return cache.volume
    market = Market.objects.get(id=market_id)
    queryset = Trade.objects.filter(time__date__gte=start,
                                    time__date__lte=end,
                                    market=market).order_by('time')
    close = queryset.last().price
    low_high = queryset.aggregate(low=Min('price'),
                                  high=Max('price'))
    MFM = ((close - low_high['low']) - (low_high['high'] - close)) /\
        (low_high['high'] - low_high['low'])
    perv_adi = 0
    if start != first:
        perv_adi = adi(start-timedelta(days=1),
                       end-timedelta(days=1),
                       market_id, first)
    if user.has_perm('index.create_adi'):
        new_adi = ADI.objects.create(start=start, end=end, volume=MFM+perv_adi)
        return new_adi.volume
    else:
        return 'You do not have permission to access this index'
