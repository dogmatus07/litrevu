"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reviews import views
from reviews.views import RegisterView, \
    LoginView, \
    home, \
    add_ticket, \
    edit_ticket, \
    list_tickets, \
    dashboard, \
    feed, delete_ticket,\
    add_review, \
    add_ticket_review, \
    list_following, unfollow_user, list_reviews
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_ticket/', add_ticket, name='add_ticket'),
    path('edit_ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', delete_ticket, name='delete_ticket'),
    path('add_review/<int:ticket_id>/', add_review, name='add_review'),
    path('add_ticket_review', add_ticket_review, name='add_ticket_review'),
    path('tickets/', list_tickets, name='list_tickets'),
    path('reviews/', list_reviews, name='list_reviews'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('feed/', feed, name='feed'),
    path('following/', list_following, name='list_following' ),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
