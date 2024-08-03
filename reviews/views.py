from django.shortcuts import render, redirect, get_object_or_404
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
        return render(request, 'reviews/register.html', {'form':form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'reviews/register.html', {'form':form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'reviews/login.html', {'form':form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Vous êtes connecté')
            return redirect('home')
        else:
            messages.error(request, 'Echec de la connexion')
        return render(request, 'reviews/login.html', {'form' : form})

@login_required
def dashboard(request):
    pass


@login_required
def list_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'reviews/list_tickets.html', {'tickets': tickets})

@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user # assign the ticket to the current user
            ticket.save()
            return redirect('home') # redirect to homepage
        else:
            print(form.errors)
    else:
        form = TicketForm
    return render(request, 'reviews/add_ticket.html', {'form': form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le billet a été modifié avec succès')
            return redirect('home')
        else:
            messages.error(request, 'Des erreurs sont présentes dans le formulaire')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})