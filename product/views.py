from django.db.models.fields import EmailField
from product.models import product
from django.shortcuts import redirect, render, get_object_or_404
from .models import BoostedItem, Jobapplication, Subcategory, product, image, Category
import operator
import functools
import logging
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
import json
from django.contrib import messages
from django.urls import reverse
from .helpers import AuthorRequiredMixin, ajax_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse,Http404
from .forms import Jobform, Productform , Productform2, Boostedform
from django.db.models import Q
from mpesa_api.core.mpesa import Mpesa
from django.utils import timezone
from sweetify.views import SweetifySuccessMixin
from django.urls import reverse_lazy


# Create your views here.


class ProductListView(ListView):
    """Basic ListView implementation to call the published articles list."""

    model = product
    paginate_by = 16
    context_object_name = "products"
    template_name = "product/products.html"

    def get_queryset(self):
        return self.model.objects.all().order_by('-timestamp')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trendings"] = self.model.objects.filter(timestamp__month=timezone.now().month)[:3]
        return context

class ProductList1(ListView):
    template_name = 'product_list.html'
    model = product
    paginate_by = 8
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        products=product.objects.filter(category=self.category.id)
        return product.objects.filter(category=self.category).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(ProductList1, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class MyProductsListView(ListView):
    """Basic ListView implementation to call the published articles list."""

    model = product
    paginate_by = 20
    context_object_name = "products"
    template_name = "product/my-products.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = "My Listings"
        return context

    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user).order_by('-timestamp')

class CreateBoostedItems(LoginRequiredMixin, CreateView):
    model= BoostedItem
    message = 'You have succesfully Boosted your product'
    form_class= Boostedform
    template_name='product/productBoost.html'



    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user

        phone = self.request.user.phone
        price = form.instance.price
        # Mpesa credantials required
        # To-Do
        # Mpesa.c2b_register_url()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("products:my_listings")


class MyActiveProductsListView(MyProductsListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = "My Active Listings"
        return context

    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user, status='OPEN').prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))


class MyDraftProductsListView(MyProductsListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = "My Draft Listings"
        return context

    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user, status='DRAFT').prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))

class MyClosedProductsListView(MyProductsListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = "My Closed Listings"
        return context

    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user, status='CLOSED').prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))


class DraftsListView(MyProductsListView):
    """Overriding the original implementation to call the drafts articles
    list."""

    def get_queryset(self, **kwargs):
        return product.objects.get_drafts()

class CreateProductView(LoginRequiredMixin,CreateView,SweetifySuccessMixin):

    model = product
    message = "Your product has been created."
    form_class = Productform
    template_name = "product/product_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user


        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("products:list")




class CreateProductView2(LoginRequiredMixin,CreateView,SweetifySuccessMixin):

    model=product
    form_class= Productform2
    template_name = 'product/product_create2.html'


    def get_object(self, queryset=None):
        return self.model.objects.get(id = self.request.session['form_data'])


    def post(self, request, *args, **kwargs):
        form = self.form_class(data = request.POST)
        if form.is_valid():
            Product = self.model.objects.get(id = request.session['product'])
            Product.Subcategory = request.POST.get('Subcategory')
            Product.Brand= request.POST.get('Brand')
            Product.Model= request.POST.get('Model')
            Product.county= request.POST.get('county')
            Product.location= request.POST.get('location')
            Product.save()
            return redirect('products:list')

        else:
            return render(request, "product/product_create2.html", {form:form})



    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("products:list")





class Jobapplicationview(LoginRequiredMixin, CreateView):
    model=Jobapplication
    message = "You have successfully posted your CV"
    form_class=Jobform
    template_name='Jobs/Jobs.html'
    def form_valid(self, form):
        form.instance.user = self.request.user


        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("products:home")




class EditProductView(AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing articles."""

    model = product
    message = "Your product has been updated."
    form_class = Productform
    template_name = "product/product_edit.html"    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['image'] = image.objects.filter(listing=self.object)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        listing = form.save(commit=True)
        images = form.cleaned_data['image']
        image_ids = json.loads(images)
        index = 0

        for im_id in image_ids:
            image = image.objects.get(id=im_id)
            image.listing = listing
            image.index = index
            image.save()
            index += 1

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("products:my_listings")

class DetailProductView(DetailView):
    """Basic DetailView implementation to call an individual product."""

    model = product

    def get_object(self):
        obj = super(DetailProductView, self).get_object()
        obj.views+=1
        obj.save
        if obj is None:
            raise Http404("Product does not exist")
        return obj


        

@login_required
@ajax_required
@require_http_methods(["POST"])
def post_image(request):
    """A function view to implement the post functionality with AJAX allowing
    to create News instances as parent ones."""

    image = request.FILES["image"]
    if image is not None:
        image = image.objects.create(image=image)

        return JsonResponse({"id": image.id})

    else:
        return HttpResponseBadRequest(
            content=_(f"No Image uploaded.")
        )

@login_required
@ajax_required
@require_http_methods(["POST"])
def delete_image(request):
    """A function view to implement the post functionality with AJAX allowing
    to create News instances as parent ones."""

    image = request.POST["image"]
    if image is not None:
        image = image.objects.filter(id=image).delete()

        return JsonResponse({"id": image})

    else:
        return HttpResponseBadRequest(
            content=_(f"No Image Id provided.")
        )

@login_required
@ajax_required
@require_http_methods(["DELETE"])
def delete_product(request, id):

    product = product.objects.filter(id=id, user=request.user).first()

    if product is not None:
        product.delete()
        return JsonResponse({"status": 200})

    else:
        return JsonResponse({"status": 403, "error": "Listing could not be found"})


@login_required
@ajax_required
@require_http_methods(["PUT"])
def close_product(request, id):

    product = product.objects.filter(id=id, user=request.user).first()

    if product is not None:

        if product.status == "CLOSED":
            return JsonResponse({"status": 403, "error": "Listing is already closed"})
        else:
            product.status = "CLOSED"
            product.save()
            return JsonResponse({"status": 200})

    else:
        return JsonResponse({"status": 403, "error": "Listing could not be found"})


@login_required
@ajax_required
@require_http_methods(["PUT"])
def publish_product(request, id):

    product = product.objects.filter(id=id, user=request.user).first()

    if product is not None:

        if product.status == "CLOSED":
            return JsonResponse({"status": 403, "error": "Listing is closed"})

        elif product.status == 200:
            return JsonResponse({"status": 403, "error": "Listing is already closed"})

        else:
            product.status = "ACTIVE"
            product.save()

            return JsonResponse({"status": 200})

    else:
        return JsonResponse({"status": 403, "error": "Listing could not be found"})







def load_subcategory(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'hr/subcategory_options.html', {'subcategories': subcategories})

def load_brand(request):
    subcategory_id= request.GET.get('Subcategory')
    brands = Subcategory.objects.filter(Subcategory_id=subcategory_id).order_by('name')
    return render(request, 'hr/subcategory_options.html', {'brands': brands})

def load_models(request):
    Brand_id = request.GET.get('Brand')
    models = Subcategory.objects.filter(Brand_id=Brand_id).order_by('name')
    return render(request, 'hr/subcategory_options.html', {'models': models})

def load_location(request):
    county_id = request.GET.get('county')
    location = Subcategory.objects.filter(county_id=county_id).order_by('name')
    return render(request, 'hr/subcategory_options.html', {'location': location})