from django import forms
from .models import Order


INPUT_CLASS = (
    "w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none "
    "focus:ring-2 focus:ring-gray-800 text-sm"
)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone",
            "address_line1", "address_line2",
            "city", "state", "postal_code", "country",
            "notes",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Phone number"}),
            "address_line1": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Street address"}),
            "address_line2": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Apt, suite (optional)"}),
            "city": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "State / Province"}),
            "postal_code": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Postal code"}),
            "country": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Country"}),
            "notes": forms.Textarea(attrs={"class": INPUT_CLASS, "rows": 3, "placeholder": "Order notes (optional)"}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["full_name"].initial = user.get_full_name()
            self.fields["email"].initial = user.email
            self.fields["phone"].initial = user.phone
            self.fields["address_line1"].initial = user.address_line1
            self.fields["address_line2"].initial = user.address_line2
            self.fields["city"].initial = user.city
            self.fields["state"].initial = user.state
            self.fields["postal_code"].initial = user.postal_code
            self.fields["country"].initial = user.country or "India"
