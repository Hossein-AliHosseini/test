from django.core.management.base import BaseCommand, CommandError
from nobitex.models import Market, Trades
import datetime
import requests
import sys
import json

class Command(BaseCommand):
    help = 'Prints Trades on Website which have existing Market in Database in Terminal'

    def handle(self, *args, **kwargs):
        all_market = Market.objects.all()
        for market in all_market:
            response = requests.get('https://api.nobitex.ir/v2/trades/' + market.__str__().replace('-', '')).text
            json_data = json.loads(response)
            all_trades = json_data['trades']
            for trade in all_trades:
                try:
                    new_trade = Trades.objects.create(time=(datetime.datetime.fromtimestamp(trade['time']//1000)), price=float(trade['price']),
                                                    volume=float(trade['volume']), type=trade['type'][0], market=market)
                    # new_trade.save()
                except:
                    sys.stdout.write('Trade with current time is already exists in database\n')