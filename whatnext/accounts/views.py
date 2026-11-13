from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! You may now log in.")
        return super().form_invalid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Error! Please correct your credentials.")
        return super().form_invalid(form)

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    model = CustomUser
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user
