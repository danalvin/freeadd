from django import forms
from django.forms.fields import ImageField

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import BoostedItem, product, image


class Productform(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = product
        fields = ["title", "Description", "category", "Subcategory", "county", "location","price", "image"]


class Boostedform(forms.ModelForm):
    def __init__(self, user,*args, **kwargs):
        super(Boostedform,self).__init__(*args, **kwargs)
        self.fields['product'].queryset = product.objects.filter(user=user)

    class Meta:
        model = BoostedItem
        fields = ["product", "type"]