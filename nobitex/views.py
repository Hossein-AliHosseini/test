from django.shortcuts import render, HttpResponse
from nobitex.forms import TradeForm
import requests
import json
import datetime

context = {}

def hello_world(request):
    form = TradeForm()
    context['form'] = form
    if request.GET:
        date = request.GET['date']
        time = datetime.datetime.fromtimestamp(int(date)/1000)
        market = request.GET['market']
        response = requests.get('https://api.nobitex.ir/v2/trades/' + market).text
        json_data = json.loads(response)
        all_trades = json_data['trades']
        temp_trades = []
        for trade in all_trades:
            trade_time = datetime.datetime.fromtimestamp(trade['time']/1000)
            print(trade_time, time)
            if trade_time == time:
                temp_trades.append(trade)
        context['valid_trades'] = temp_trades
    return render(request, 'date_market_view.html', context)


def trade_table(request):
        return render(request, 'table_view.html', context)