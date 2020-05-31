# Changed News to Favorite
from django.contrib import admin
from bootcamp.favorites.models import Favorites


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "reply")
    list_filter = ("timestamp", "reply")
