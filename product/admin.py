from product.models import product, image
from django.contrib import admin
from product.models import *
# Register your models here.


@admin.register(product)      
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'price')

@admin.register(image)
class ProductimageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'index')