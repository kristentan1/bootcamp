# Changed News to Research
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ResearchConfig(AppConfig):
    name = "bootcamp.research" # changed from name = "bootcamp.news"
    verbose_name = _("Research")
