from django.contrib import admin
from .models import Experience, Content

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

    list_filter = (
        "category",
    )

@admin.register(Content)
class ContentsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "explanation",
        "details",
    )