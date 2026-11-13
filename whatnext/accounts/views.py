from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! You may now log in.")

    def form_invalid(self, form):
        messages.success(self.request, "Error! Please correct your credentials.")
        return super().form_invalid(form)
