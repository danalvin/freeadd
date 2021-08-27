from django import forms

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import product, image


class Productform(forms.ModelForm):
    images = forms.CharField(min_length=3)
    class Meta:
        model = product
        fields = ["title", "Description", "category", "county", "location","price", "images", "tags"]
