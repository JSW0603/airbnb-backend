from django.contrib import admin
from .models import Room, Amenity

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "city",
        "type",
        "rooms",
        "owner",
        "created_at",
    )

    list_filter = (
        "city",
        "type",
        "rooms",
        "amenities",
    )

@admin.register(Amenity)
class Amenity(admin.ModelAdmin):
    
    list_display = (
        "name",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
