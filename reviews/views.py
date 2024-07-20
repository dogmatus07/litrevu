from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from .models import Ticket, Review

def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'reviews/home.html', {'tickets': tickets, 'reviews': reviews})

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'reviews/register.html', {'form' : form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'reviews/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'reviews/login.html', {'form' : form})

    def post(self, request):
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'reviews/login.html', {'form' : form})
