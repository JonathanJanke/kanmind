from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "fullname", "is_staff", "is_active")
    search_fields = ("email", "fullname")
    ordering = ("email",)
    readonly_fields = ("password",)
