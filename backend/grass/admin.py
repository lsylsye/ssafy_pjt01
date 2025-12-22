from django.contrib import admin
from .models import GrassDaily


@admin.register(GrassDaily)
class GrassDailyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date", "points", "updated_at")
    list_filter = ("date",)
    search_fields = ("user__username", "user__nickname")
