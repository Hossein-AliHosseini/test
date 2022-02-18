from django.utils.timezone import now
from django.shortcuts import render, HttpResponse

from nobitex.models import Trades, Market
from nobitex.forms import TradeForm
from nobitex.tables import TradesTable, ChartTable
from nobitex.tasks import create_chart


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
    queryset = create_chart.delay(date.strftime("%Y-%m-%d %H:%M:%S"), market.id).get()
    table = ChartTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'candlestick_charts.html', {
        'form': form,
        'table': table,
    })
