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
from reviews.views import RegisterView, LoginView, home, add_ticket, edit_ticket, list_tickets, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('add_ticket/', add_ticket, name='add_ticket'),
    path('edit_ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('tickets/', list_tickets, name='list_tickets'),
    path('dashboard/', dashboard, name='dashboard')

]
