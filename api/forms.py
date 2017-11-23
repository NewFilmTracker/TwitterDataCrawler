from django import forms
import datetime

class QueryForm(forms.Form):
    query = forms.CharField(required=True, max_length=100)
    lang = forms.ChoiceField(widget = forms.Select(),
    choices = ([('en','en'), ('id','id')]), initial='en', required=True)
    count = forms.IntegerField(required=True, min_value = 1, max_value = 100)

class ReleaseForm(forms.Form):
    start = forms.DateField(required=True, initial=datetime.date.today, input_formats=['%Y-%m-%d'])
    end = forms.DateField(required=True, initial=datetime.date.today, input_formats=['%Y-%m-%d'])

class FilmSearchForm(forms.Form):
    query = forms.CharField(required=True, max_length=100)
    