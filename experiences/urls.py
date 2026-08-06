from django.urls import path
from .views import Contents, ContentDetail

urlpatterns = [
    path("Contents/", Contents.as_view()),
    path("Contents/<int:pk>/", ContentDetail.as_view()),
]