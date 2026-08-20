from rest_framework import serializers
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from reviews.serializers import ReviewSerializer
from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlists

"""
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 #django의 프레임워크가 depth를 1로 설정하면 RoomSerializer가 Room 객체를 serialize할 때, Room에 연결된 Amenity 객체도 함께 serialize하도록 설정
"""
# depth를 1로 설정하면 지나치게 많은 데이터가 노출이 되어서 다시 작은 Room list serializer 생성 
class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )

class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField() #RoomDetailSerializer에 rating 필드를 추가하고, 해당 필드의 값을 get_rating 메서드를 통해 계산하도록 설정
    is_owner = serializers.SerializerMethodField() #RoomDetailSerializer에 is_owner 필드를 추가하고, 해당 필드의 값을 get_is_owner 메서드를 통해 계산하도록 설정
    is_liked = serializers.SerializerMethodField()
    reviews = ReviewSerializer(read_only=True, many=True)
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context.get('request')

        if not request.user.is_authenticated:
            return False
        
        return Wishlists.objects.filter(
            user=request.user, 
            rooms__pk=room.pk
        ).exists()


class RoomListSerializer(serializers.ModelSerializer):

    rating = serializers.SerializerMethodField() #RoomListSerializer에 rating 필드를 추가하고, 해당 필드의 값을 get_rating 메서드를 통해 계산하도록 설정
    is_owner = serializers.SerializerMethodField() #RoomListSerializer에 is_owner 필드를 추가하고, 해당 필드의 값을 get_is_owner 메서드를 통해 계산하도록 설정
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "type",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context.get("request")
        return room.owner == request.user
        
