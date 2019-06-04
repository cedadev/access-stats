from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime, timedelta

class FilterForm(forms.Form):
    start = forms.DateField(widget=DatePickerInput(format="%Y/%m/%d"),label="Start date:", required=False, input_formats=["%Y/%m/%d"], initial=(datetime.now()-timedelta(days=90)).strftime("%Y/%m/%d"))
    end = forms.DateField(widget=DatePickerInput(format="%Y/%m/%d"),label="End date:", required=False, input_formats=["%Y/%m/%d"], initial=(datetime.now()).strftime("%Y/%m/%d"))
    dataset = forms.CharField(max_length=100, required=False, label="Dataset:", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":""}))
