from rest_framework import serializers #REST API -> 백엔드 핵심 구문

class CategorySerializer(serializers.Serializer):

    pk = serializers.IntegerField() #자동으로 db에서 데이터 로딩
    name = serializers.CharField(required = True)
    kind = serializers.CharField()
    created_at = serializers.DateTimeField()

