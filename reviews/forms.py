from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Ticket, Review
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user. Extends UserCreationForm to include first name and last name
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Facultatif')
    last_name = forms.CharField(max_length=30, required=False, help_text='Facultatif')
    class Meta(UserCreationForm.Meta):
        """
        Meta class to specify the model to be used and the fields to be included
        """
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture')

    def save(self, commit=True):
        """
        Method to save first name, last name and the standard fields
        Args:
            commit (bool): Commit the save operation (default is True)
        Returns:
            CustomUser: Created user instance
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomUserAuthenticationForm(AuthenticationForm):
    """
    Authentification form for existing users (username = email)
    """
    class Meta:
        """
        Meta Class to specify the model to use and the fields to be included
        """
        model = CustomUser
        fields = ('email', 'password')

class TicketForm(forms.ModelForm):
    """
    Form to create or update a ticket. Allows input for: title, description and image.
    """
    class Meta:
        """
        Meta Class to specify the model to use and the fields to be included.
        """
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du billet'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'row': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'required': True}),
        }

class ReviewForm(forms.ModelForm):
    """
    Form to create reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre critique', 'rows': 5}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la critique'})
        }

class TicketReviewForm(forms.ModelForm):
    """
    Form to create a ticket and its review combined
    """
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

class TicketandReviewForm(forms.Form):
    """
    Form to add ticket and review for the this ticket
    """
    # ticket = TicketReviewForm()
    # review = ReviewForm()
    def __init__(self, *args, **kwargs):
        super(TicketandReviewForm, self).__init__(*args, **kwargs)
        self.ticket_form = TicketForm(*args, **kwargs, prefix='ticket')
        self.review_form = ReviewForm(*args, **kwargs, prefix='review')

    def is_valid(self):
        return self.ticket_form.is_valid() and self.review_form.is_valid()

    def save(self, commit=True):
        ticket = self.ticket_form.save(commit=False)
        review = self.review_form.save(commit=False)
        if commit:
            ticket.save()
            review.ticket = ticket
            review.save()
        return ticket, review

User = get_user_model()

class FollowUserForm(forms.Form):
    """
    Form to follow a user
    """
    username = forms.CharField(max_length=150, label="Nom d'utilisateur à suivre")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            user_to_follow = User.objects.get(email=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas")
        return user_to_follow
