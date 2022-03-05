import django_tables2 as tables

from index.models import MA, EMA, SO, ADI


class MATable(tables.Table):

    class Meta:
        model = MA
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'Please wait to calculate Moving Average...'


class EMATable(tables.Table):

    class Meta:
        model = EMA
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'Please wait to calculate Exponential Moving Average...'


class SOTable(tables.Table):

    class Meta:
        model = SO
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'Please wait to calculate Stochastic Oscillator...'


class ADITable(tables.Table):

    class Meta:
        model = ADI
        template_name = 'django_tables2/bootstrap4.html'
        empty_text = 'Please wait to calculate Accumulation/Distribution Indicator...'
