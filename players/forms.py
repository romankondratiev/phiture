from django import forms
# from .utils import team_builder

class TeamForm(forms.Form):
    budget = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":'Enter your budget in Euros'}))


