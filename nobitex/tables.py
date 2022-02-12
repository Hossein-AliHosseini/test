import django_tables2 as tables

from nobitex.models import Trades, Tradeee

class TradesTable(tables.Table):
    class Meta:
        model = Trades
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No trades for given market and date!!!'

class ChartTable(tables.Table):
    class Meta:
        model = Tradeee
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No data for given market and date!!!'