from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm, TicketForm
from .models import Ticket, Review

def home(request):
    login_form = CustomUserAuthenticationForm()
    register_form = CustomUserCreationForm()
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'tickets': tickets,
        'reviews': reviews
    }
    return render(request, 'reviews/home.html', context)

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

@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        form = TicketForm
    return render(request, 'reviews/add_ticket.html', {'form': form})