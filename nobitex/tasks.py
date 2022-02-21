from celery import shared_task

from django.db.models import Min, Max, DateTimeField
from django.db.models.functions import Trunc

from nobitex.models import Trades, Market


@shared_task
def store_trades(market):
    queryset = Trades.objects.filter(market__id=market).values()
    file_obj = open('trades.txt', 'a')
    for query in queryset:
        file_obj.write(str(query) + "\n")


@shared_task
def create_chart(date, market_id):
    market = Market.objects.get(id = market_id)
    queryset = Trades.objects.filter(time__gte=date, market=market).\
                    annotate(start_time=Trunc('time', 'hour', output_field=DateTimeField())).order_by('start_time').\
                        values('start_time').\
                            annotate(low=Min('price'), high=Max('price'), open_time=Min('time'), close_time=Max('time'))

    for query in queryset:
        query['open'] = Trades.objects.filter(time=query['open_time']).first().price
        query['close'] = Trades.objects.filter(time=query['close_time']).first().price

    return queryset[:]
