from django import forms

class ShtoLiberForm(forms.Form):
    liber_id = forms.IntegerField(label='liber_id', required=True, widget=forms.HiddenInput())

class HiqLiberForm(forms.Form):
    liber_id = forms.IntegerField(label='liber_id', required=True, widget=forms.HiddenInput())