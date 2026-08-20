from django.urls import path
from .views import Wishlists, WishListDetail, WishListToggle

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk>", WishListDetail.as_view()),
    path("<int:pk>/rooms/<int:room_pk>", WishListToggle.as_view()),
]