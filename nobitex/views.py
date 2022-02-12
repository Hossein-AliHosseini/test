from django.utils.timezone import now
from django.shortcuts import render, HttpResponse
from django.db.models import Min, Max

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
    queryset = Trades.objects.select_related('market').filter(time=date)
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
    time_step = 15
    queryset = Trades.objects.filter(time__gte=date, market=market).order_by('time')
    table_list = []
    table_dict = {}
    if queryset.exists():
        last_trade = queryset.last()
        while True:
            start_end = queryset.filter(time__lt=date+timedelta(minutes=time_step),
                                        time__gte=date).order_by('time')
            if start_end.exists():
                table_dict['open'] = str(start_end.first().price)
                table_dict['close'] = str(start_end.last().price)
                table_dict['start_time'] = str(date)
                table_dict['end_time'] = str(date+timedelta(minutes=time_step))
                min_max = start_end.aggregate(min_value=Min('price'),
                                              max_value=Max('price'))
                table_dict['low'] = min_max['min_value']
                table_dict['high'] = min_max['max_value']
                table_list.append(copy.deepcopy(table_dict))
            if last_trade.time <= date:
                break
            else:
                date += timedelta(minutes=time_step)
    table = ChartTable(table_list)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'candlestick_charts.html', {
        'form': form,
        'table': table,
    })
