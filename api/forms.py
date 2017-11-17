from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(required=True, max_length=100)
    lang = forms.ChoiceField(widget = forms.Select(),
    choices = ([('en','en'), ('id','id')]), initial='en', required=True)