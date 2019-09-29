from django import forms
# from .utils import team_builder

class TeamForm(forms.Form):
    budget = forms.IntegerField(max_value=99999999999999999999, widget=forms.TextInput(attrs={"placeholder":'Enter your budget in €'}))


