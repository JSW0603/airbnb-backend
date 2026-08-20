from rest_framework.serializers import ModelSerializer
from rooms.serializer import RoomListSerializer
from .models import Wishlists

class WishlistSerializer(ModelSerializer):
    rooms = RoomListSerializer(
        many=True,
        read_only=True,
    )

class WishlistsSerializer(ModelSerializer):
    class Meta:
        model = Wishlists
        fields = (
            "pk",
            "name",
            "rooms",
        )


