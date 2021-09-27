
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from users.models import User
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import AuthenticationForm



class Registrationform(BSModalModelForm,UserCreationForm):


    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2', 'phone']
        error_messages = {
            'first_name': {
                'required': 'First name is required',
                'max_length': 'Name is too long'
            },
            'last_name': {
                'required': 'Last name is required',
                'max_length': 'Last Name is too long'
            },
            'username': {
                'required': 'Username is required',
                 'max_length': 'Last Name is too long',
                 'unique': "A user with that username already exists.",
            }
        }




class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")
            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user
