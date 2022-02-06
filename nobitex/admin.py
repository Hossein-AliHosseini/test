from django.contrib import admin
from nobitex.models import Market, Trades


admin.site.register(Market)
admin.site.register(Trades)

# command for printing markets from db
# command for getting trades from nobitex site (for existing markets)
