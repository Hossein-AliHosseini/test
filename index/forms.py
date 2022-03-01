from django import forms

from nobitex.models import Market


class Type1Form(forms.Form):
    start = forms.DateField()
    end = forms.DateField()
    market = forms.ModelChoiceField(queryset=Market.objects.all())


class Type2Form(forms.Form):
    start = forms.DateField()
    market = forms.ModelChoiceField(queryset=Market.objects.all())
