from rest_framework import serializers #REST API -> 백엔드 핵심 구문
from .models import Category 

class CategorySerializer(serializers.ModelSerializer): #ModelSerializer을 활용한 코드 간소화
    class Meta:
        model = Category
        fields = "__all__" #만약 Category 모델의 모든 필드를 serializer에 포함시키고 싶다면, "__all__"을 사용하면 됨. 제외하고 싶은게 있을경우, exclude 를 사용.
    