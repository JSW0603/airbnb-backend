from django.contrib import admin
from .models import Review

# Register your models here.
class WordFilter(admin.SimpleListFilter): #simplelistfilter 제목이 필요
    title = "Filter by words"
    parameter_name = "word"
    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, queryset):
        word = self.value()
        if word:
            return Review.filter(payload__contains=word)
        else:
            Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host", #reviews에 모델파일에 user 항목에 연결한 foreign key를 이용해서 검색가능
        "room__type", #항목__필터 원하는 항목으로 설정
    )

