# Changed News to Research
from django.contrib import admin
from bootcamp.internship.models import Internship


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "reply")
    list_filter = ("timestamp", "reply")
