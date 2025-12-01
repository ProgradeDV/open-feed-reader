"""Forms."""
from typing import ClassVar

from django import forms

from feeds.models import Source


class EditFeedForm(forms.ModelForm):
    """form for creating a new source or edit existing source."""

    class Meta:  # noqa: D106
        model = Source
        fields:ClassVar[list] = ["name", "title", "site_url", "feed_url", "image_url", "description"]

    def __init__(self, *args:any, **kwargs:any) -> None:  # noqa: D107
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            # if 'class' not in field.widget.attrs:
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "placeholder"
