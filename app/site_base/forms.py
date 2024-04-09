"""site_base.forms"""
from django import forms


class SearchForm(forms.Form):
    """the form for subscribing to a new source"""
    search_text = forms.CharField(label="Search", max_length=512, required=False)
