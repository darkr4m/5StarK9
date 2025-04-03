from django.contrib import admin
from .models import User

# Register your models here.
# admin.site.register([User])
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # --- List View Customization (Client list page) ---
    list_display = ('last_name', 'first_name', 'email', 'user_type', 'is_active')
    list_filter = ['user_type','is_active']
    search_fields = ('last_name', 'email',)  # Enable searching across these fields
    ordering = ('last_name', 'first_name') # Default sorting 
    # --- Change/Add Form Customization (Client detail page) ---
    fieldsets = (
        # Section 1: Basic Info
        ('Basic Info', {
            'fields': ('first_name', 'last_name', 'email', 'date_joined')
        }),
        # Section 2: Status & Notes
        ('Status and Roles', {
            'fields' : ['is_active', 'is_staff', 'is_staff_member', 'user_type'],
            'classes': ['collapse'] # Makes the section collapsible
        })
    )
    readonly_fields = ['date_joined']
    