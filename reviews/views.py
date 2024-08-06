from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm, TicketForm
from .models import Ticket, Review, UserFollows
from django.contrib import messages

def home(request):
    """
    Homepage view that displays login form and registration invite.
    If user is authenticated, redirect to dashboard

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object with the homepage template rendered includes context data
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

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
    """
    View for handling registration process
    Methods: GET and POST
    """
    def get(self, request):
        """
        Handle GET request to show the registration form
        """
        form = CustomUserCreationForm()
        return render(request, 'reviews/register.html', {'form':form})

    def post(self, request):
        """
        Handle POST request to process the registration form data
        """
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'reviews/register.html', {'form':form})

class LoginView(View):
    """
    View for handling user login
    Methods: GET and POST
    """
    def get(self, request):
        """
        Handle the GET request to show the login form
        """
        form = AuthenticationForm()
        return render(request, 'reviews/login.html', {'form':form})

    def post(self, request):
        """
        Handle the POST request to process the login form data
        """
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Vous êtes bien connecté')
                return redirect('dashboard')
            else:
                messages.error(request, 'Echec de la connexion, identifiant à vérifier')
        else:
            messages.error(request, 'Login failed. Please try again.')

        return render(request, 'reviews/login.html', {'form' : form})

@login_required
def dashboard(request):
    """
    Dashboard view that displays user dashboard

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object with the dashboard template rendered includes context data
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    context = {
        'tickets': tickets,
        'reviews' : reviews
    }
    return render(request, 'reviews/dashboard.html', context)

@login_required
def feed(request):
    """
    View to get :
        the actual user,
        followed users,
        ticket of the user and the followed users,
        reviews of the tickets,

    Returns: HttpRequest, context data
    """
    user = request.user
    followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)
    tickets = Ticket.objects.filter(user__in=followed_users).order_by('-time_created')
    reviews = Review.objects.filter(ticket__user__in=followed_users).order_by('-time_created')

    context = {
        'tickets': tickets,
        'reviews': reviews
    }
    return render(request, 'reviews/feed.html', context)


@login_required
def list_tickets(request):
    """
    View to list the tickets created by the logged-in user
    """
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'reviews/list_tickets.html', {'tickets': tickets})

@login_required
def add_ticket(request):
    """
    View to add a new ticket.
    Methods: GET and POST
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user # assign the ticket to the current user
            ticket.save()
            return redirect('dashboard') # redirect to dashboard
        else:
            print(form.errors)
    else:
        form = TicketForm
    return render(request, 'reviews/add_ticket.html', {'form': form})


@login_required
def edit_ticket(request, ticket_id):
    """
    View to edit an existing ticket. Validate if the ticket belong to the logged-in user
    """
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

@login_required
@require_POST
def delete_ticket(request, ticket_id):
    """
    View to delete a ticket owned by a logged in user
    Require POST method for security
    Require that the user is authenticated
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Billet supprimé avec succès')
        return redirect('dashboard')
    else:
        messages.error(request, 'Erreur lors de la suppression')
        return redirect('dashboard')
