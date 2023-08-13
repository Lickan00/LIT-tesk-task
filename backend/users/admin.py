from django.contrib import admin

from .models import User


class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'confirmation_code',
        'password'
    )


admin.site.register(User, AdminUser)
