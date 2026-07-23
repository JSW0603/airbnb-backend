from django.db import models
from common.models import CommonModel
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Review(CommonModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE,)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.SET_NULL,)
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE,)
    payload = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
        ]
    )

    def __str__(self) -> str:
        return f"{self.user} / {"⭐️"*self.rating} ({self.rating})"