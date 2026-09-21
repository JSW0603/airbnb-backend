from rest_framework.serializers import ModelSerializer
from .models import Content, Experience

class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"

class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        exclude = (
            "id",
            "created_at",
            "updated_at",
            "host",
            "category",
            "contents"
        )