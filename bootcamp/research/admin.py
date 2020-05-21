# Changed News to Research
from django.contrib import admin
from bootcamp.research.models import Research


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "reply")
    list_filter = ("timestamp", "reply")
