from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Ticket, Review

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

class ReviewForm(forms.ModelForm):
    """
    From to create reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
            'rating': forms.RadioSelect(),
        }