from django.utils.timezone import now
from django.shortcuts import render, HttpResponse
from django.db.models import Min, Max, DateTimeField, Count, F, Case, When, Value, CharField, Q, FloatField
from django.db.models.functions import Trunc

from nobitex.models import Trades, Market
from nobitex.forms import TradeForm
from nobitex.tables import TradesTable, ChartTable

from datetime import timedelta

import copy


def hello_world(request):
    return HttpResponse('<h1>Hello World!</h1>')


def view_trades(request):
    form = TradeForm(request.GET)
    if form.is_valid():
        market = form.cleaned_data['market']
        date = form.cleaned_data['date']
    else:
        market = Market.objects.first()
        date = now().date()
        form = TradeForm(initial={
            'date': date,
            'market': market,
        })
    queryset = Trades.objects.select_related("market").filter(time__date=date, market=market)
    table = TradesTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'view_trades.html', {
        'form': form,
        'table': table,
    })


def candlestick_charts(request):
    form = TradeForm(request.GET)
    if form.is_valid():
        market = form.cleaned_data['market']
        date = form.cleaned_data['date']
    else:
        market = Market.objects.first()
        date = now().date()
        form = TradeForm(initial={
            'date': date,
            'market': market,
        })
    time_step = 1
    queryset = Trades.objects.filter(time__gte=date, market=market).\
        annotate(start_time=Trunc('time', 'hour', output_field=DateTimeField())).order_by('start_time').\
            values('start_time').\
                annotate(low=Min('price'), high=Max('price'), open=Min('time'), close=Max('time'))
                    # annotate(open=Case(When(open_time=F('time'), then=F('price')), output_field=FloatField()),
                    #         close=Case(When(close_time=F('time'), then=F('price')), output_field=FloatField()))
    table = ChartTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'candlestick_charts.html', {
        'form': form,
        'table': table,
    })
