from django import forms
from VolleyballApp.database import selections
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, max_length=512)
    password = forms.CharField(widget=forms.PasswordInput, max_length=512)

class AddPlayerForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, max_length=512)
    password = forms.CharField(widget=forms.TextInput, max_length=512)
    name = forms.CharField(widget=forms.TextInput, max_length=512)
    surname = forms.CharField(widget=forms.TextInput, max_length=512)
    date_of_birth = forms.CharField(widget=forms.TextInput, max_length=512)
    height = forms.CharField(widget=forms.TextInput, max_length=512)
    weight = forms.CharField(widget=forms.TextInput, max_length=512)
    positions = forms.MultipleChoiceField(choices=selections.get_positions(), widget=forms.CheckboxSelectMultiple(attrs={"class": "posSelect"}))
    teams = forms.MultipleChoiceField(choices=selections.get_teams(), widget=forms.CheckboxSelectMultiple(attrs={"class": "teamSelect"}))

class AddCoachJuryForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, max_length=512)
    password = forms.CharField(widget=forms.TextInput, max_length=512)
    name = forms.CharField(widget=forms.TextInput, max_length=512)
    surname = forms.CharField(widget=forms.TextInput, max_length=512)
    nationality = forms.CharField(widget=forms.TextInput, max_length=512)

class StadiumForm(forms.Form):
    stads = selections.get_stadiums()
    to_tuple = []
    for i in stads:
        to_tuple.append((i["stadium_ID"], i["stadium_name"]))
    Stadium = forms.ChoiceField(choices=tuple(to_tuple), widget= forms.Select)
    New_Stadium_Name = forms.CharField(widget=forms.TextInput, max_length=512)

class DeleteMatchForum(forms.Form):
    Session_ID= forms.CharField(widget=forms.TextInput, max_length=512)