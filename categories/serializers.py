from rest_framework import serializers #REST API -> 백엔드 핵심 구문
from .models import Category 

class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField(read_only=True) #자동으로 db에서 데이터 로딩
    name = serializers.CharField(max_length=15, required = True,)
    kind = serializers.ChoiceField(choices=Category.CategoryKindChoices.choices,)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data): #class를 통해서 만든 데이터와 serializer을 통해서 얻은 validated data를 같이 합침.
        return Category.objects.create(**validated_data) #**는 딕셔너리를 가져옴

    def update(self, instance, validated_data):
        instance.name = validated_data("name", instance.name) #instance.name은 default 값을 현재값으로 보내도록 설정
        instance.kind = validated_data("kind", instance.kind)
        instance.save()
        return instance