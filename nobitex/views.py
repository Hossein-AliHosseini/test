from django.utils.timezone import now
from django.shortcuts import render, HttpResponse
from django.db.models import Min, Max

from nobitex.models import Trades, Market, Tradeee
from nobitex.forms import TradeForm
from nobitex.tables import TradesTable, ChartTable

from datetime import timedelta


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
    Tradeee.objects.all().delete()
    time_step = 15
    queryset = Trades.objects.select_related('market').filter(time__gte=date).order_by('time')
    if queryset.exists():
        last_trade = queryset.last()
        while True:
            min_max = queryset.aggregate(min_value=Min('price'), max_value=Max('price'))
            start_end = queryset.filter(time__lt=date+timedelta(minutes=time_step), time__gte=date).order_by('time')
            if start_end.exists():
                Tradeee(start_date=date, end_date=date+timedelta(minutes=time_step), min=min_max['min_value'], max=min_max['max_value'], start=start_end.first().price, end=start_end.last().price).save()
            if last_trade.time <= date:
                break
            else:
                date = date + timedelta(minutes=time_step)
    table = ChartTable(Tradeee.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'candlestick_charts.html', {
        'form': form,
        'table': table,
    })
