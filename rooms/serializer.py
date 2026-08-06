from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer

"""
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        depth = 1 #django의 프레임워크가 depth를 1로 설정하면 RoomSerializer가 Room 객체를 serialize할 때, Room에 연결된 Amenity 객체도 함께 serialize하도록 설정
"""
# depth를 1로 설정하면 지나치게 많은 데이터가 노출이 되어서 다시 작은 Room list serializer 생성 
class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )

class RoomDetailSerializer(ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"



class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "type",
        )
        
