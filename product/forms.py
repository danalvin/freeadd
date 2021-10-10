from django import forms
from django.db.models import fields
from django.forms.fields import ImageField

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField
from tinymce.widgets import TinyMCE

from .models import BoostedItem, Brand, Jobapplication, Subcategory, area, product, image, Model


class Productform(forms.ModelForm):
    image = forms.ImageField()
    Description = forms.CharField(widget=TinyMCE())
    class Meta:
        model = product
        fields = ["title", "Description", "category", "Subcategory", "Brand", "Model", "county", "location","price", "image", "image2", "image3"]
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['Subcategory'].queryset = Subcategory.objects.none()
    #     self.fields['Brand'].queryset = Brand.objects.none()
    #     self.fields['Model'].queryset = Model.objects.none()
    #     self.fields['location'].queryset = area.objects.none()


class Boostedform(forms.ModelForm):
    def __init__(self, user,*args, **kwargs):
        super(Boostedform,self).__init__(*args, **kwargs)
        self.fields['product'].queryset = product.objects.filter(user=user)

    class Meta:
        model = BoostedItem
        fields = ["product", "type"]


class Jobform(forms.ModelForm):
    class Meta:
        model=Jobapplication
        fields=['name', 'jobgroup', 'CV']