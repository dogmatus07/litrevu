from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import View
from .forms import CustomUserCreationForm, \
    CustomUserAuthenticationForm, \
    TicketForm, \
    ReviewForm, \
    TicketReviewForm,TicketandReviewForm, \
    FollowUserForm
from .models import Ticket, Review, UserFollows
from django.contrib import messages
from django.forms import FileInput
from django.db.models import Count

@login_required
def follow_user(request):
    """
    View for following user based on username (email)

    :param request:
    """
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            try:
                user_to_follow = form.cleaned_data['username']
                if user_to_follow == request.user:
                    messages.warning(request, 'Vous ne pouvez pas vous suivre vous-même')
                elif UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                    messages.warning(request, f'Vous suivez déjà '
                                              f'{user_to_follow.first_name} {user_to_follow.last_initial}.')
                else:
                    UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                    messages.success(request, f'Vous suivez maintenant '
                                              f'{user_to_follow.first_name} {user_to_follow.last_initial}.')
            except CustomUser.DoesNotExist:
                    messages.warning(request, "Cet utilisateur n'existe pas")
            return redirect('follow_user')
    else:
        form = FollowUserForm()
    return render(request, 'reviews/follow_user.html', {'form': form})

@login_required
def list_following(request):
    """
    View for listing all the users followed by request.user (and vice versa), and follow new users
    :param request:
    """
    following = UserFollows.objects.filter(user=request.user).prefetch_related('followed_user').annotate(
        ticket_number=Count('followed_user__ticket')
    )
    followers = UserFollows.objects.filter(followed_user=request.user).prefetch_related('user').annotate(
        ticket_number=Count('user__ticket')
    )

    form = FollowUserForm()
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            user_to_follow = form.cleaned_data['username']
            if user_to_follow != request.user and not UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                messages.success(
                    request, f'Vous suivez maintenant '
                             f'{user_to_follow.first_name} '
                             f'{user_to_follow.last_initial}.')
            else:
                messages.warning(
                    request, f'Vous suivez déjà '
                             f'{user_to_follow.first_name} {user_to_follow.last_initial}.'
                )
            return redirect('list_following')

    return render (request, 'reviews/list_following.html', {
        'following': following,
        'followers': followers,
        'form': form
    })

@login_required
@require_POST
def unfollow_user(request, user_id):
    """
    View to handle unfollow user actions.

    :param request:
    :param user_id:
    """
    user_to_unfollow = get_object_or_404(UserFollows, user=request.user, followed_user_id=user_id)
    user_to_unfollow.delete()
    messages.success(request, f'Vous ne suivez plus cet utilisateur: {user_to_unfollow}')
    return redirect('list_following')


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
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
    tickets = Ticket.objects.filter(user__in=followed_users).prefetch_related('reviews__user').order_by('-time_created')
    ticket_ids = tickets.values_list('id', flat=True)
    reviewed_tickets_ids = Review.objects.filter(ticket__in=tickets).values_list('ticket_id', flat=True).distinct()

    context = {
        'tickets': tickets,
        'reviewed_tickets_ids': set(reviewed_tickets_ids)
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
            return redirect('dashboard')
        else:
            messages.error(request, 'Des erreurs sont présentes dans le formulaire')
    else:
        form = TicketForm(instance=ticket)
        form.fields['image'].widget = FileInput()

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

@login_required
def add_review(request, ticket_id):
    """
    View to add a new review on a ticket
    :param request:
    :param ticket_id:
    :return:
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Votre avis a été publié avec succès')
            return redirect('dashboard')
        else:
            messages.error(request, 'Des erreurs sont présentes dans ce formulaire')
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'ticket': ticket
    }
    return render(request, 'reviews/add_review.html', context)

def add_ticket_review(request):
    if request.method == 'POST':
        form = TicketandReviewForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.cleaned_data['ticket'].save(commit=False)
            ticke.user = request.user
            ticket.save()

            review = form.cleaned_data['review'].save(commit=False)
            review.user = request.user
            review.save()

            return redirect('dashboard')
    else:
        form = TicketandReviewForm()

    return render(request, 'reviews/add_ticket_review.html', {'form': form})
