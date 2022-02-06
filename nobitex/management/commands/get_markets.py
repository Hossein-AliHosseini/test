from django.core.management.base import BaseCommand, CommandError
from nobitex.models import Market
import sys


class Command(BaseCommand):
    help = 'Prints Markets in DataBase in Terminal'

    def handle(self, *args, **kwargs):
        all_market = Market.objects.all()
        for market in all_market:
            sys.stdout.write(market.__str__() + '\n')
