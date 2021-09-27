from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.urls import reverse, reverse_lazy
from django.db.models import Prefetch
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from users.forms import Registrationform, UserLoginForm
from bootstrap_modal_forms.generic import BSModalLoginView
from django.http import JsonResponse




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
        "username",
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
        return reverse("products:list")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


def register(request):
  if request.method == 'POST':
    # Get form values
    first_name = request.POST['first_name']
    email = request.POST['email']
    phone = request.POST['phone']
    # Set The username to be the phone number
    username = phone
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check if passwords match
    if password == password2:
      # Check username
      if User.objects.filter(username=username).exists():
        messages.error(request, 'That username is taken')
        return redirect('users:register')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'That email is being used')
          return redirect('users:register')
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, phone=phone)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('users:login')
    else:
      messages.error(request, 'Passwords do not match')
      return redirect('users:register')
  else:
    return render(request, 'accounts/register.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'You are now logged in')
      return redirect('products:list')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('users:login')
  else:
    return render(request, 'accounts/login.html')



class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


