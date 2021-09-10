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


class registerUser(CreateView):
    model = User
    form_class = Registrationform
    template_name = 'account/register.html'
    success_url = '/edit-profile'
    

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/employee/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/products'
    authentication_form = UserLoginForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('products:list')

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)