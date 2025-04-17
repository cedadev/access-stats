from django import forms
from django.conf import settings
from common.date_form import DateForm


class FilterForm(DateForm):
    if not settings.PUBLIC_SITE:
        user = forms.CharField(
            required=False,
            label="User:",
            widget=forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
        )
    dataset = forms.CharField(
        required=False,
        label="Dataset:",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
    )
    method = forms.CharField(
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
    bots = forms.ChoiceField(
        choices=[
            ("remove-bots", "Bots filtered"),
            ("allow-bots", "Bots allowed"),
        ],
        required=False,
        label="Bot type (not yet functional, does nothing):",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": ""}),
    )
