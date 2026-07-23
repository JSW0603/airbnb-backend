from django.contrib import admin
from .models import ChattingRoom, Message

# Register your models here.
@admin.register(ChattingRoom)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
    )
#rooms 에서 Room 이라는 모델이 있어서 오류 발생 -> 모두 user를 통해서 모두 연결이 되어있음. Room -> ChattingRoom 으로 변경

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "user",
        "room",
        "created_at",
    )

    list_filter = (
        "created_at",
    )
