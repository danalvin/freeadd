from product.models import product, image
from django.contrib import admin
from product.models import *
# Register your models here.


@admin.register(product)      
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'price')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'Category', 'slug')

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    
@admin.register(area)
class areaAdmin(admin.ModelAdmin):
    list_display = ('name', 'County', 'slug')

admin.site.register(image)
admin.site.register(BoostedItem)

admin.site.register(BoostedType)