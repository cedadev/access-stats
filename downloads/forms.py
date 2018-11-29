from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class FilterForm(forms.Form):
    start = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"),label='Start date:', required=False)
    end = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d"),label='End date:', required=False)
    user = forms.CharField(max_length=100, required=False, label="User:", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":""}))
    dataset = forms.CharField(max_length=100, required=False, label="Dataset:", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":""}))
    method = forms.CharField(max_length=100, required=False, label="Method:", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":""}))
    anon = forms.ChoiceField(choices=[("all","All"),("only-anon","Only Anonymous Users"),("non-anon","Registered Users")], required=False, label="User type:", widget=forms.Select(attrs={"class": "form-control", "placeholder":""}))
