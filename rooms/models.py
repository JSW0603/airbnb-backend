from django.db import models
from common.models import CommonModel
from django.db.models import Avg

# Create your models here.
class Room(CommonModel):
    
    class RoomKindChoices(models.TextChoices):
        ENTIRE_HOUSE = ("entire_house", "Entire House",)
        PRIVATE_ROOM = ("private_room", "Private Room",)
        SHARED_ROOM = ("shared_room", "Shared Room",)

    name = models.CharField(max_length=50, default="",)
    country = models.CharField(max_length=50, default="Spain",)
    city = models.CharField(max_length=80, default="Madrid",)
    price = models.PositiveBigIntegerField()
    rooms = models.PositiveBigIntegerField()
    toilet = models.PositiveBigIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=200)
    pet = models.BooleanField(default=True)
    type = models.CharField(max_length=15, choices=RoomKindChoices.choices,)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="rooms",)
    amenities = models.ManyToManyField("rooms.Amenity", related_name="rooms",)
    category = models.ForeignKey(
            "categories.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="rooms",
        ) #related_name 을 추가함으로써, 데이터베이스 조회가 좀 더 수월해짐

    def __str__(self) -> str:
        return self.name

    def total_amenities(self):
        return self.amenities.count()

    def rating(self): #게시물에 평균평점 추가하는 기능. 
        average_rating = self.reviews.aggregate(Avg("rating"))['rating__avg']
        if average_rating is None:
            return "No Reviews"
        else:
            return round(average_rating,2)


class Amenity(CommonModel):

    """ Amenity Definition """
    name = models.CharField(max_length=100,)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"