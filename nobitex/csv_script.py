import datetime
import csv

from django.utils.timezone import make_aware

from nobitex.models import Market, Trades


def run():
    Trades.objects.all().delete()
    with open('nobitex/data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        markets = list(Market.objects.all())

        def get_market(market_string):
            market = next(
                (m for m in markets if str(m) == market_string),
                None,
            )
            if market is None:
                base_asset, quote_asset = market_string.split('-')
                market = Market.objects.create(
                    base_asset=base_asset,
                    quote_asset=quote_asset
                )
                markets.append(market)
            return market
        all_trades = []
        for row in csv_reader:
            market = get_market(row[0])
            new_trade = Trades(
                time=(make_aware(datetime.datetime.
                                 fromtimestamp(float(row[4])))),
                price=float(row[2]),
                volume=float(row[3]),
                type=row[1],
                market=market,
            )
            all_trades.append(new_trade)
            if len(all_trades) < 1000:
                continue
            Trades.objects.bulk_create(all_trades)
            all_trades = []
        Trades.objects.bulk_create(all_trades)


run()
