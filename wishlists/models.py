from django.db import models
from common.models import CommonModel

# Create your models here.
class Wishlists(CommonModel):
    name = models.CharField(max_length=150,)
    rooms = models.ManyToManyField("rooms.Room", blank=True,)
    experiences = models.ManyToManyField("experiences.Experience", blank=True,)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE,) #유저는 많은 위시리스트를 가져갈 수 있지만, 위시리스트는 한명의 유저밖에 가지지 못하도록 설정

    def __str__(self) -> str:
        return self.name