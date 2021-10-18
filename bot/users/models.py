from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

MY_CHOICES = (
    (1, "Вариант №1"),
    (2, "Вариант №2"),
    (3, "Вариант №3"),
)
# Create your models here.
class Profile(models.Model):
    chat_id = models.IntegerField()
    tg_login = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(null=True, blank=True)
    answer = MultiSelectField(choices=MY_CHOICES)

    def __str__(self):
        return f"User {self.name} with id {self.chat_id}"
    
