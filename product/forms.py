from django import forms
from django.forms.fields import ImageField

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import product, image


class Productform(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = product
        fields = ["title", "Description", "category", "Subcategory", "county", "location","price", "image"]
