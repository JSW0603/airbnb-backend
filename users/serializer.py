from rest_framework.serializers import ModelSerializer
from .models import User

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "profile_picture",
            "username",
        )

class PrivateUserSerializer(ModelSerializer): #API View에서 사용되는 Serializer
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "first_name",
            "last_name",
        ) #USER API View에서 사용되는 Serializer는 PrivateUserSerializer, 언급한 필드는 제외됩니다.