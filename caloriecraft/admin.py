from django.contrib import admin

from .models import FoodHistory, Pantry

admin.site.register(FoodHistory)


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "user")
    search_fields = ("name",)
    list_filter = ("name", "user")
    ordering = ("name",)
