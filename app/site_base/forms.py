"""site_base.forms"""
from django import forms


class SourceSearchForm(forms.Form):
    """the form for subscribing to a new source"""
    search_text = forms.CharField(label="Search", max_length=512, required=False)



class EditSourceForm(forms.Form):
    """form for creating a new source or edit existing source"""
    name = forms.CharField(max_length=255, required=False)
    site_url = forms.URLField(max_length=255, required=False)
    feed_url = forms.URLField(max_length=512)
    image_url = forms.URLField(max_length=512, required=False)

    description = forms.CharField(required=False)
    interval = forms.IntegerField(min_value=0)
