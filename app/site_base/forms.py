"""site_base.forms"""
from django import forms


class NewSubscriptionForm(forms.Form):
    """the form for subscribing to a new source"""
    feed_url = forms.CharField(label="Feed URL", max_length=512)
