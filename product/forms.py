from django import forms

from markdownx.fields import MarkdownxFormField
from multiupload.fields import MultiImageField

from .models import product, image


class Productform(forms.ModelForm):
    images = forms.CharField(min_length=3)
    class Meta:
        model = product
        fields = ["title", "Description", "category", "Subcategory", "county", "location","price", "images"]

    def is_valid(self):
        valid = super(Productform, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(Productform, self).save(commit=False)
        if commit:
            job.save()
        return job
