from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TLUser
from django.utils.translation import gettext_lazy as _


@admin.register(TLUser)
class TLUserAdmin(UserAdmin):
    model = TLUser
    list_display = ('email', 'tel', 'nick', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'tel', 'nick', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'tel', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'nick')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'tel', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
