from rest_framework.decorators import api_view #rest_framework 로딩에 문제 발생 -> pylance에서 찾지못함 -> python 인터프리터의 로딩위치 문제
from rest_framework.response import Response #Python: Select Interpreter 를 통해서 위치 변경
from rest_framework.viewsets import ModelViewSet
from .models import Category
from .serializers import CategorySerializer

# Create your views here.
class CategoryViewSet(ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
