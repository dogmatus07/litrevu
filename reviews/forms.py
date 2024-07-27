from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Ticket

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Facultatif')
    last_name = forms.CharField(max_length=30, required=False, help_text='Facultatif')
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
