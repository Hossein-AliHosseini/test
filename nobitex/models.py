from django.db import models
from django.contrib import messages
from django.conf import settings
# from django.db.models import loading
# from django.core.management import call_command

class Market(models.Model):
    base_asset = models.CharField(max_length=8)
    quote_asset = models.CharField(max_length=8)
    
    def save(self, *args, **kwargs):
        for field_name in ['base_asset', 'quote_asset']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.upper())
        super(Market, self).save(*args, **kwargs)

    
    # def cli_print_market(self):
    #     loading.cache.loaded = False
    #     call_command('print_market')
        
    
    class Meta:
        unique_together = ('base_asset', 'quote_asset')
    
    def __str__(self):
        return self.base_asset + '-' + self.quote_asset



class Trade(models.Model):
    # time = models.DateTimeField(unique=True)
    time = models.BigIntegerField(unique=True)
    price = models.FloatField()
    volume = models.FloatField()
    type = models.CharField(max_length=1)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.market) + '-' + self.type
    
    
    
