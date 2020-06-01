# Changed News to Research
from django.contrib import admin
from bootcamp.community.models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("content", "user", "reply")
    list_filter = ("timestamp", "reply")
