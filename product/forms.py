from django import forms
from django.db.models import fields
from django.forms.fields import ImageField

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import BoostedItem, Brand, Jobapplication, Subcategory, area, product, image, Model


class Productform(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = product
        fields = ["title", "Description", "category", "Subcategory", "Brand", "Model", "county", "location","price", "image", "image2", "image3"]


class Productform2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Productform2, self).__init__(*args, **kwargs)
        self.fields['category'].label = "category"
        self.fields['Subcategory'].label = "Subcategory"
        self.fields['Brand'].label = "Brand"
        self.fields['Model'].label = "Model"
        self.fields['county'].label = "County"
        self.fields['location'].label = "location"
        self.fields['image'].label = " Product Image"
        self.fields['image2'].label = "Product image"
        self.fields['image3'].label = "Product Image"


    class Meta:
        model = product
        fields = ["category", "Subcategory", "Brand", "Model", "county", "location", "image", "image2", "image3"]

    def is_valid(self):
        valid = super(Productform2, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        Product = super(Productform2, self).save(commit=False)
        
        if commit:
            return Product.save()
        return Product


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