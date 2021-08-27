from .models import product, image
from django.db.models import Prefetch
from django.shortcuts import render, redirect


def home_view(request):
    """Basic ListView implementation to call the published articles list."""

    products = product.objects.filter(status="OPEN").prefetch_related(Prefetch("images", queryset=image.objects.order_by( "index"), to_attr="image"))

    latest_listing = product.objects.filter(status="OPEN").order_by('timestamp')[:10].prefetch_related(
        Prefetch("image",
                 queryset=image.objects.order_by("index"),
                 to_attr="image"))

    return render(request, 'pages/home.html', {'products': products, 'latest': latest_listing})


def dashboard_view(request):
    return render(request, 'users/user-home.html')
