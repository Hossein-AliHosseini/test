from celery import shared_task

from django.db.models import Avg

from nobitex.models import Trades
# save data after calculation


@shared_task
def ma(start, end):
    queryset = Trades.objects.filter(time__date__gte=start,
                                     time__date__lte=end).\
                                         aggregate(moving_average=Avg('price'))
    return queryset['moving_average']


@shared_task
def ema(start, end):
    pass


@shared_task
def so(start):
    pass


@shared_task
def adi(start, end):
    pass
