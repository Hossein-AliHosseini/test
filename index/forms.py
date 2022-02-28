from django import forms


class Type1Form(forms.Form):
    start = forms.DateField()
    end = forms.DateField()


class Type2Form(forms.Form):
    start = forms.DateField()
