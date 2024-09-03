from django.contrib import admin
from .models import CustomUser, Ticket, Review

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    search_fields = ('email',)
    list_filter = ('is_active', 'is_staff')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')
    search_fields = ('title', 'description')
    list_filter = ('time_created',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'rating', 'time_created')
    search_fields = ('body',)
    list_filter = ('time_created', 'rating')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
