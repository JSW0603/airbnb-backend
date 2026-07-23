from django.contrib import admin
from .models import Wishlists

# Register your models here.
@admin.register(Wishlists)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )