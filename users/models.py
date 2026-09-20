from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
    
    class LanguageChoices(models.TextChoices):
        ENGLISH = "en", "English"
        SPANISH = "es", "Spanish"
        FRENCH = "fr", "French"
        GERMAN = "de", "German"
        ITALIAN = "it", "Italian"
        PORTUGUESE = "pt", "Portuguese"
        RUSSIAN = "ru", "Russian"
        CHINESE = "zh", "Chinese"
        JAPANESE = "ja", "Japanese"
        KOREAN = "ko", "Korean"

    class CurrencyChoices(models.TextChoices):
        USD = "usd", "USD"
        EUR = "eur", "EUR"
        GBP = "gbp", "GBP"
        JPY = "jpy", "JPY"
        CNY = "cny", "CNY"
        INR = "inr", "INR"
        RUB = "rub", "RUB"
        BRL = "brl", "BRL"
        CAD = "cad", "CAD"
        AUD = "aud", "AUD"

    first_name = models.CharField(max_length=140, default="",)
    last_name = models.CharField(max_length=140, default="",)
    name = models.CharField(max_length=140, default="",)
    profile_picture = models.URLField(blank=True) #blank=True means that the field is optional
    is_host = models.BooleanField(default=False,)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices,) #choices=GenderChoices.choices means that the field can only take values from the Gender
    language = models.CharField(max_length=2, choices=LanguageChoices.choices,)
    currency = models.CharField(max_length=3, choices=CurrencyChoices.choices,)
