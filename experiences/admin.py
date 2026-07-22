from django.contrib import admin
from .models import Experience, Contents

# Register your models here.
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "country",
        "starts_at",
        "end",
    )

@admin.register(Contents)
class ContentsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "explanation",
        "details",
    )