# Changed News to Favorite
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FavoritesConfig(AppConfig):
    name = "bootcamp.favorites" # changed from name = "bootcamp.news"
    verbose_name = _("Favorites")
