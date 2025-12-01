"""Site base Forms."""
from django import forms


class SearchForm(forms.Form):
    """Form for subscribing to a new source."""

    search_text = forms.CharField(label="Search", max_length=512, required=False)
