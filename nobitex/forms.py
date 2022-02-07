from django import forms

from nobitex.models import Market


class TradeForm(forms.Form):
    date = forms.DateField()
    market = forms.ModelChoiceField(queryset=Market.objects.all())
