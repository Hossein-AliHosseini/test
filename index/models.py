from django.db import models

from nobitex.models import Market


class MA_Base(models.Model):  # (Simple) Moving Average
    start = models.DateField()
    end = models.DateField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('start', 'end')

    def __str__(self):
        return "MA-" + str(self.start) + " " + str(self.end)


class MA(models.Model):
    base = models.ForeignKey(MA_Base, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    value = models.FloatField()


class EMA_Base(models.Model):  # Exponential Moving Average
    start = models.DateField()
    end = models.DateField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('start', 'end')

    def __str__(self):
        return "EMA-" + str(self.start) + " " + str(self.end)


class EMA(models.Model):
    base = models.ForeignKey(EMA_Base, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    value = models.FloatField()


class SO_Base(models.Model):  # Stochastic Oscillator
    start = models.DateField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('start',)

    def __str__(self):
        return "SO-" + str(self.start)


class SO(models.Model):
    base = models.ForeignKey(SO_Base, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    value = models.FloatField()


class ADI_Base(models.Model):  # Accumulation/Distribution Indicator
    start = models.DateField()
    end = models.DateField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('start', 'end')

    def __str__(self):
        return "ADI-" + str(self.start)


class ADI(models.Model):
    base = models.ForeignKey(ADI_Base, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    value = models.FloatField()
