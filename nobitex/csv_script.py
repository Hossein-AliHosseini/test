import datetime
import csv
from nobitex.models import Market, Trades


def find_market(market_name):
    for market in Market.objects.all():
        if market.__str__() == market_name:
            return market
    return None


def run():
    Trades.objects.all().delete()
    with open('nobitex/data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        all_trades = []
        for row in csv_reader:
            new_trade = Trades(datetime.datetime.fromtimestamp(int(float(row[4]))), float(row[2]),
                            float(row[3]), row[1], find_market(row[0]))
            all_trades.append(new_trade)
        Trades.objects.bulk_create(all_trades)

