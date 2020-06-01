# Changed News to Community
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CommunityConfig(AppConfig):
    name = "bootcamp.community" # changed from name = "bootcamp.news"
    verbose_name = _("Community")
