"""site_base.forms"""
from django import forms


class SourceSearchForm(forms.Form):
    """the form for subscribing to a new source"""
    search_text = forms.CharField(label="Search", max_length=512, required=False)



class EditSourceForm(forms.Form):
    """form for creating a new source or edit existing source"""
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    site_url = forms.URLField(max_length=255, required=False, widget=forms.URLInput(attrs={'class': "form-control"}))
    feed_url = forms.URLField(max_length=512, widget=forms.URLInput(attrs={'class': "form-control"}))
    image_url = forms.URLField(max_length=512, required=False, widget=forms.URLInput(attrs={'class': "form-control"}))

    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': "form-control"}))
    interval = forms.IntegerField(min_value=0, initial=100, widget=forms.NumberInput(attrs={'class': "form-control"}))
