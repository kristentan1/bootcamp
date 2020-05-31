# Changed News to Internship
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InternshipConfig(AppConfig):
    name = "bootcamp.internship" # changed from name = "bootcamp.news"
    verbose_name = _("Internship")
