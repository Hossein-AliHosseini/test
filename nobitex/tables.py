import django_tables2 as tables
import itertools

from nobitex.models import Trades

class TradesTable(tables.Table):
    class Meta:
        model = Trades
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'No trades for given market and date!!!'

class ChartTable(tables.Table):
    low = tables.Column()
    high = tables.Column()
    open = tables.Column()
    close = tables.Column()
    start_time = tables.Column()
    end_time = tables.Column()


    def render_low(self, value):
        return '| %s |' % value

    def render_high(self, value):
        return '| %s |' % value

    def render_open(self, value):
        return '| %s |' % value

    def render_close(self, value):
        return '| %s |' % value

    def render_start_time(self, value):
        return '| %s |' % value

    def render_end_time(self, value):
        return '| %s |' % value