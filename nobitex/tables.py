import django_tables2 as tables

from nobitex.models import Trades


class TradesTable(tables.Table):
    class Meta:
        model = Trades
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No trades for given market and date!!!'


class ChartTable(tables.Table):
    low = tables.Column(verbose_name='lowest price')
    high = tables.Column(verbose_name='highest price')
    open = tables.Column(verbose_name='opening price')
    close = tables.Column(verbose_name='closing price')
    start_time = tables.Column()

    class Meta:
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No trades for given market and date!!!'

    def render_low(self, value):
        return value

    def render_high(self, value):
        return value

    def render_open(self, value):
        return value

    def render_close(self, value):
        return value

    def render_start_time(self, value):
        return value
