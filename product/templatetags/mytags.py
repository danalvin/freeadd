from django import template
from product.models import Category
from django.db.models import Count

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag('_categorieslist.html')
def show_categories():
    categories = Category.objects.annotate(product_count=Count("product")).filter(product_count__gt=0).order_by('-product_count','name') 
    #categories = Category.objects.annotate(post_count=Count("blog_posts")).filter(post_count__gt=0).order_by('name')
    # categories = Category.objects.all().order_by('name')
    return{'categories': categories}

@register.inclusion_tag('_categoriessidelist.html')
def show_categories_side():
    categories = Category.objects.annotate(product_count=Count("product")).filter(product_count__gt=0).order_by('-product_count','name') 
    return{'categories': categories}

@register.inclusion_tag('accounts/login.html')
def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('dashboard')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')
