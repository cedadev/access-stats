from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime, timedelta
from common.date_form import DateForm

class FilterForm(DateForm):
    dataset = forms.CharField(max_length=100, required=False, label="Dataset:", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":""}))
