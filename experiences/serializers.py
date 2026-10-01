from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.serializer import TinyUserSerializer
from medias.serializers import PhotoSerializer
from categories.serializers import CategorySerializer
from wishlists.models import Wishlists
from .models import Content, Experience

class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"

class ExperienceSerializer(ModelSerializer):

    is_host = TinyUserSerializer(read_only=True)

    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        exclude = (
            "created_at",
            "updated_at",
            "category",
            "contents"
        )

    def get_is_host(self, obj):
        request = self.context.get("request")
        if request:
            return obj.host == request.user
        return False

class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        fields = "__all__"

    def get_is_host(self, obj):
        request = self.context.get("request")
        if request:
            return obj.host == request.user
        return False

    def get_is_liked(self, experience):
        request = self.context.get["request"]
        return Wishlists.objects.filter(user=request.user, experiences=experience).exists()
