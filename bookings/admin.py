from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = (
        "kind",
        "user",
        "room",
        "experience",
        "experience_time",
        "check_in",
        "check_out",
        "guests",
    )