import strawberry
from . import models
from strawberry import auto

@strawberry.django.type(models.Review)
class ReviewType:
    id: auto
    payload: auto
    rating: auto