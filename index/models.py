from django.db import models


class MA(models.Model):  # (Simple) Moving Average
    start = models.DateField()
    end = models.DateField()
    volume = models.FloatField()

    def __str__(self):
        return "MA-" + str(self.start) + " " + str(self.end)


class EMA(models.Model):  # Exponential Moving Average
    start = models.DateField()
    end = models.DateField()
    volume = models.FloatField()

    def __str__(self):
        return "EMA-" + str(self.start) + " " + str(self.end)


class SO(models.Model):  # Stochastic Oscillator
    start = models.DateField()
    volume = models.FloatField()

    def __str__(self):
        return "SO-" + str(self.start)


class ADI(models.Model):  # Accumulation/Distribution Indicator
    start = models.DateField()
    end = models.DateField()
    volume = models.FloatField()

    def __str__(self):
        return "ADI-" + str(self.start)
