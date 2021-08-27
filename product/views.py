from product.models import product
from django.shortcuts import render
from .models import product, image, Category
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
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import Productform
from django.db.models import Q


# Create your views here.


class ProductListView(ListView):
    """Basic ListView implementation to call the published articles list."""

    model = product
    paginate_by = 15
    context_object_name = "products"
    template_name = "product/products.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        county = self.request.GET.get("county", "ALL")
        context["page_title"] = county + " LISTINGS"
        return context

    def get_queryset(self, **kwargs):
        queryset = product.objects.filter(status="OPEN")
        queryset = self.query_category(queryset)
        queryset = self.query_county(queryset)
        queryset = self.query_title(queryset)
        queryset = self.query_sort(queryset)
        return queryset.prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))

    def query_category(self, queryset):
        categories = self.request.GET.getlist("category", default=[cat.value for cat in Category])
        q_list = []

        for category in categories:
            q_list.append(Q(category=category))

        return queryset.filter(functools.reduce(operator.or_, q_list))

    def query_county(self, queryset):
        county = self.request.GET.get("county", "ALL")
        if county == 'ALL':
            return queryset
        else:
            return queryset.filter(county=county)

    def query_title(self, queryset):
        title = self.request.GET.get("title", "")

        return queryset.filter(Q(title__contains=title) | Q(location__contains=title) | Q(tags__name=title)).distinct()

    def query_sort(self, queryset):
        sort = self.request.GET.get("sort", "timestamp")
        if sort == "price_desc":
            return queryset.order_by("-price")
        elif sort == "price_asc":
            return queryset.order_by("price")
        elif sort == "popularity":
            return queryset.order_by("bookmarks")
        # TODO: check how to sort once bookmarks are implemented.
        else:
            return queryset.order_by("timestamp")

class MyProductsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published articles list."""

    model = product
    paginate_by = 10
    context_object_name = "articles"
    template_name = "product/my-products.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = "My Listings"
        return context

    def get_queryset(self, **kwargs):
        return product.objects.filter(user=self.request.user).prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))

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

class CreateProductView(LoginRequiredMixin, CreateView):

    model = product
    message = "Your product has been created."
    form_class = Productform
    template_name = "product/product_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        listing = form.save(commit=True)
        images = form.cleaned_data['images']
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
        return reverse("produts:my_listings")

class EditProductView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
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

class DetailProductView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual product."""

    model = product

    def get_object(self):
        obj = super().get_object()
        obj.views+=1
        obj.save
        return obj


    def get_queryset(self):
        queryset = super(DetailProductView, self).get_queryset()
        return queryset.prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))
        

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
