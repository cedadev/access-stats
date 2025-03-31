from django import forms
from django.conf import settings
from common.date_form import DateForm


class FilterForm(DateForm):
    if not settings.PUBLIC_SITE:
        user = forms.CharField(
            max_length=100,
            required=False,
            label="User:",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
        )
    dataset = forms.CharField(
        max_length=100,
        required=False,
        label="Dataset:",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
    )
    method = forms.CharField(
        max_length=100,
        required=False,
        label="Method:",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
    )
    anon = forms.ChoiceField(
        choices=[
            ("all", "All"),
            ("anon", "Only Anonymous Users"),
            ("non-anon", "Registered Users"),
        ],
        required=False,
        label="User type:",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": ""}),
    )
