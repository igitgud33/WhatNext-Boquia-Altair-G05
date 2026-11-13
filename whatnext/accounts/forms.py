from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data["email"]

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.validationError("This email is already registered.")

        return email