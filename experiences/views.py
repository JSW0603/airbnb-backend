from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Content
from .serializers import ContentSerializer

# Create your views here.
class Contents (APIView):
    def get(self, request):
        all_contents = Content.objects.all()
        serializer = ContentSerializer(all_contents, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            return Response(ContentSerializer(content).data)
        else:
            return Response(serializer.errors)

class ContentDetail (APIView):
    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise NotFound
        
    def get(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            updated_content = serializer.save()
            return Response(ContentSerializer(updated_content).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete
        return Response(status=HTTP_204_NO_CONTENT)