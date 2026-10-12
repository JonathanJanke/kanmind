from django.contrib import admin
from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner_id",
        "member_count",
        "ticket_count",
        "tasks_to_do_count",
        "tasks_high_prio_count",
    )
    search_fields = ("title",)
