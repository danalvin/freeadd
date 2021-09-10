from django import template
from product.models import Category
from django.db.models import Count

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('_categorieslist.html')
def show_categories():
    categories = Category.objects.annotate(product_count=Count("blog")).filter(post_count__gt=0).order_by('-post_count','title') 
    #categories = Category.objects.annotate(post_count=Count("blog_posts")).filter(post_count__gt=0).order_by('name')
    # categories = Category.objects.all().order_by('name')
    return{'categories': categories}