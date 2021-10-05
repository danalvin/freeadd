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
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(JobGroup)
@admin.register(Jobapplication)
class JobapplicationAdmin(admin.ModelAdmin):
    list_filter=['user','jobgroup']
    list_display=['user','jobgroup']


from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"