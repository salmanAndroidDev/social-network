from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
        Register Post for admin panel
    """
    list_display = ('title', 'user', 'policy')
    list_editable = ('policy',)
