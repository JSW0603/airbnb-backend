from rest_framework.decorators import api_view #rest_framework 로딩에 문제 발생 -> pylance에서 찾지못함 -> python 인터프리터의 로딩위치 문제
from rest_framework.response import Response #Python: Select Interpreter 를 통해서 위치 변경
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
        Category.objects.create(
            name = request.data['name'],
            kind = request.data["kind"],
        )
        return Response({"created": True})

@api_view()
def category(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

