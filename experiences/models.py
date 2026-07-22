from django.db import models
from common.models import CommonModel

# Create your models here.
class Experience(CommonModel):
    country = models.CharField(max_length=50, default="Spain",)
    city = models.CharField(max_length=80, default="Madrid",)
    name = models.CharField(max_length=250,)
    host = models.ForeignKey("users.User", on_delete=models.CASCADE,)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=150,)
    starts_at = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    contents = models.ManyToManyField("experiences.Contents",)

    def __str__(self) -> str:
        return self.name


class Contents(CommonModel):

    name = models.CharField(max_length=100,)
    details = models.CharField(max_length=200,blank=True, null=True, default="",)
    explanation = models.TextField(blank=True, default="",)

    def __str__(self) -> str:
        return self.name

