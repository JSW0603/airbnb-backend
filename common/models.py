from django.db import models

# Create your models here.

# 데이터베이스에 추가하지 않을 model 생성 (단순 다른 model 에서 재사용할 abstract model 생성)
class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add 필드의 값을 해당 object가 처음 생성되었을 때, 시간으로 설정
    updated_at = models.DateTimeField(auto_now=True) #auto_now 해당 object가 새로 저장될 때마다, 해당 날짜와 시간으로 설정

    class Meta:
        abstract = True