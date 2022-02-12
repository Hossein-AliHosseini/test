from django import forms

from nobitex.models import Market


class TradeForm(forms.Form):
    date = forms.DateTimeField()
    market = forms.ModelChoiceField(queryset=Market.objects.all())
