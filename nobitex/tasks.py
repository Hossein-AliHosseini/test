from celery import shared_task
from nobitex.models import Trades


@shared_task
def store_trades(market):
    queryset = Trades.objects.filter(market_id=market).values()
    file_obj = open('trades.txt', 'a')
    for query in queryset:
        file_obj.write(str(query) + "\n")