from .forms import UserLoginForm
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import login

class LoginFormMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # if the top login form has been posted
        if request.method == 'POST' and 'is_top_login_form' in request.POST:

            # validate the form
            form = UserLoginForm(data=request.POST)
            if form.is_valid():

                # log the user in
                
                login(request, form.get_user())

                # if this is the logout page, then redirect to /
                # so we don't get logged out just after logging in
                if '/logout/' in request.get_full_path():
                    return HttpResponseRedirect('/')

        else:
            form = UserLoginForm(request)

        # attach the form to the request so it can be accessed within the templates
        request.login_form = form