import django_tables2 as tables

from nobitex.models import Trades

class TradesTable(tables.Table):
    class Meta:
        model = Trades
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No trades for given market and date!!!'