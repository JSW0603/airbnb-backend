from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from django.db import transaction
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Content, Experience
from categories.models import Category
from .serializers import ContentSerializer, ExperienceSerializer

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

class Experiences (APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind != Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("The category kind should be 'experience'.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    contents = request.data.get("contents")
                    for content in contents:
                        content_obj = Content.objects.get(pk=content)
                        experience.contents.add(content_obj)
                    serializer = ExperienceSerializer(experience)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Content not found.")
        else:
            return Response(serializer.errors)
                    

class ExperienceDetail (APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        