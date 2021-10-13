from django import template
from product.models import BoostedItem, Category, product
from django.db.models import Count

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('_categorieslist.html')
def show_categories():
    # categories = Category.objects.annotate(product_count=Count("product")).filter(product_count__gt=0).order_by('-product_count','name') 
    #categories = Category.objects.annotate(post_count=Count("blog_posts")).filter(post_count__gt=0).order_by('name')
    categories = Category.objects.all().order_by('name')
    return{'categories': categories}

@register.inclusion_tag('_categoriessidelist.html')
def show_categories_side():
    categories = Category.objects.annotate(product_count=Count("product")).filter(product_count__gt=0).order_by('-product_count','name') 
    return{'categories': categories}


@register.inclusion_tag('boosteditems.html')
def showboosted():
  products=BoostedItem.objects.order_by('-timestamp')
  return{'products':products}

@register.inclusion_tag('_homeadspace.html')
def adspace():
    pass