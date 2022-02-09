from django.utils.timezone import now
from django.shortcuts import render, HttpResponse

from nobitex.models import Trades, Market
from nobitex.forms import TradeForm
from nobitex.tables import TradesTable


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
    queryset = Trades.objects.select_related('market').filter(time__date=date)
    table = TradesTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=50)
    return render(request, 'view_trades.html', {
        'form': form,
        'table': table,
    })
