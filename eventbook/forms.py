from django import forms

class EventCreateView(forms.Form):
    name = forms.CharField()
