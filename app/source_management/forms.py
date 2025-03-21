"""site_base.forms"""
from django import forms
from feeds.models import Source


class EditSourceForm(forms.ModelForm):
    """form for creating a new source or edit existing source"""

    class Meta:
        model = Source
        fields = ["name", "title", "site_url", "feed_url", "image_url", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            # if 'class' not in field.widget.attrs:
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = 'placeholder'
