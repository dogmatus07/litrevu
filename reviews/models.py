from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserManager(BaseUserManager):
    """
    Custom user manage. To create normal users and superusers
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a normal user with his email and password

        Args:
            email (str) : email of the user
            password (str): password of the user

        Returns:
            CustomUser : the user instance created

        Raise:
            ValueError : Raises error if email field is not set
        """
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with his email and password.

        Args:
            email (str): email of the superuser
            password (str): password of the superuser
            extra-fields : additional fields to add to the superuser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that extends the AbstractBaseUser and PermissionsMixin
    Uses email as username
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Returns a string representation of the CustomUser
        Returns:
            str: email of the user
        """
        return self.email


    @property
    def last_initial(self):
        """

        :return: First letter of the last name of a user to preserve privacy
        """
        return self.last_name[0] if self.last_name else ''

class Ticket(models.Model):
    """
    Model that represents a ticket.
    Can contain image, title and description
    """
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tickets_media', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    """
    Model that represents a review.
    Includes a rating and text content.

    """
    ratings = [
        (1, '1 - Très mauvais'),
        (2, '2 - Mauvais'),
        (3, '3 - Moyen'),
        (4, '4 - Bon'),
        (5, '5 - Excellent')
    ]
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],\
        choices=ratings)
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

class UserFollows(models.Model):
    """
    Model that represents the following relationship between users.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
