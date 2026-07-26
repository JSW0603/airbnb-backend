from django.contrib import admin
from .models import Room, Amenity

# Register your models here.
@admin.action(description="Set all prices to zero")
def reset_price(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "city",
        "type",
        "rating",
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

    search_fields = ("name", "price",) #startwith -> ^ (ex, ^name) / exactly same data -> =

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
