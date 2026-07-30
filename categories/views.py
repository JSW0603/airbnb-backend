from rest_framework.decorators import api_view #rest_framework 로딩에 문제 발생 -> pylance에서 찾지못함 -> python 인터프리터의 로딩위치 문제
from rest_framework.response import Response #Python: Select Interpreter 를 통해서 위치 변경
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from .models import Category
from .serializers import CategorySerializer

# Create your views here.
@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True) #serializer는 Django Python에서 Json으로 변경,  
        return Response(serializer.data) #마찬가지로 user에게서 온 data를 받아서 우리의 데이터베이스에 넣을 수 있는 Django객체로 변경
    elif request.method =="POST":
        serializer = CategorySerializer(data=request.data) #CategorySerializer를 통해서 얻은 데이터를 가지고 옮
        if serializer.is_valid():
            new_category = serializer.save() #해당 데이터가 만든 조건문을 충족시, serializer는 자동으로 create 메서드를 찾기 시작함. 
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data, partial=True,) #partial로 인해서, put 하는 데이터가 완벽한 형태가 아닐수도 있음을 알림
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
