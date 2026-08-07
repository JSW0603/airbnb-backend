from django.db import models
from common.models import CommonModel

# Create your models here.
class Photo(CommonModel):
    file = models.URLField() #URLField는 URL을 저장하는 필드로, 사진 파일의 URL을 저장하는 데 사용
    description = models.CharField(max_length=100,)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE, null=True, blank=True,)
    experience = models.ForeignKey("experiences.Experience", on_delete=models.CASCADE, null=True, blank=True,)

    def __str__(self):
        return "Photo File"

class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE,)
    #하나의 게시물당 비디오는 하나만.
    
    def __str__(self):
        return "Video File"