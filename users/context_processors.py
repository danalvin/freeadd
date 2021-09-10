from .forms import Registrationform, UserLoginForm


def add_my_login_form(request):
    return {
        'login_form': UserLoginForm(data=request.POST),
    }

def add_my_registration_form(request):
    return {
        'registration_form': Registrationform(),
    }