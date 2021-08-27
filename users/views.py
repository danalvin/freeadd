from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from .models import User
from product.models import product, image

# Create your views here.



class UserDetailView(LoginRequiredMixin, ListView):
    model = product
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    context_object_name = "products"
    paginate_by = 6
    slug_url_kwarg = "username"
    template_name = "users/user_detail.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["object"] = User.objects.filter(username=self.kwargs[self.slug_url_kwarg]).get()
    #     return context

    def get_queryset(self):
        queryset = product.objects.filter(user__username=self.kwargs[self.slug_url_kwarg])
        queryset = self.query_sort(queryset)
        return queryset.prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))

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



class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})



class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "email",
        "name",
        "phone",
        "website",
        "picture",
        "about",
    ]
    model = User


    def get_queryset(self):
        queryset = product.objects.filter(user__username=self.kwargs[self.slug_url_kwarg])
        queryset = self.query_sort(queryset)
        return queryset.prefetch_related(Prefetch("images", queryset=image.objects.order_by("index"), to_attr="image"))

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
