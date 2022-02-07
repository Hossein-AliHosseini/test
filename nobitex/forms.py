from django import forms


class TradeForm(forms.Form):
    date = forms.CharField()
    market = forms.CharField()