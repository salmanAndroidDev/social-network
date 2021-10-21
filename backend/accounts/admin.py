from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User, Contact


class UserAdmin(BaseUserAdmin):
    """
        User admin panel
    """

    def follower_count(self, obj):
        return obj.following.count()

    ordering = ['id']
    list_display = ['email', 'name', 'status', 'follower_count']
    list_editable = ['status']
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (_('Personal Info'), {"fields": ('name', 'status')}),
        (_('Permissions'),
         {"fields": ('is_active', 'is_staff', 'is_superuser')}
         ),
        (_('Important dates'), {"fields": ('last_login',)})
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )


# register user for admin panel
admin.site.register(User, UserAdmin)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
        Register Contact for admin panel to define following system
    """
    pass
