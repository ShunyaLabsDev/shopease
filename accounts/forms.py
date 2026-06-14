from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none "
                "focus:ring-2 focus:ring-gray-800 text-sm"
            )


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none "
                "focus:ring-2 focus:ring-gray-800 text-sm"
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name", "last_name", "phone",
            "address_line1", "address_line2",
            "city", "state", "postal_code", "country", "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none "
                "focus:ring-2 focus:ring-gray-800 text-sm"
            )
