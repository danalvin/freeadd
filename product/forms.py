from django import forms
from django.db.models import fields
from django.forms.fields import ImageField

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import BoostedItem, Brand, Jobapplication, Subcategory, area, product, image, Model



class Productform1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Productform1, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Title"
        self.fields['Description'].label = "Product Description"
        self.fields['category'].label = "category"
        self.fields['price'].label = "Price"
        self.fields['image'].label = " Product Image"
        self.fields['image2'].label = "Product image"
        self.fields['image3'].label = "Product Image"
        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter Title',
            }
        )
        self.fields['Description'].widget.attrs.update(
            {
                'placeholder': 'Enter Description',
            }
        )
        self.fields['category'].widget.attrs.update(
            {
                'placeholder': 'Enter Category',
            }
        )
        self.fields['price'].widget.attrs.update(
            {
                'placeholder': 'Enter product price',
            }
        )

    class Meta:
        model = product
        fields = ["title", "Description", "category","price", "image", "image2", "image3"]

    def is_valid(self):
        valid = super(Productform1, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        Product = super(Productform1, self).save(commit=False)
        
        if commit:
            return Product.save()
        return Product


class Productform2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Productform2, self).__init__(*args, **kwargs)
        self.fields['Subcategory'].label = "Subcategory"
        self.fields['Brand'].label = "Brand"
        self.fields['Model'].label = "Model"
        self.fields['county'].label = "County"
        self.fields['location'].label = "location"


    class Meta:
        model = product
        fields = ["Subcategory", "Brand", "Model", "county", "location"]

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