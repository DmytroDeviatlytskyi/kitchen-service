from django.contrib.auth.models import AbstractUser
from django.db import models

from kitchen_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def str(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField()

    class Meta:
        ordering = ("username", )


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes"
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    class Meta:
        ordering = ("name", )

    def str(self):
        return f"{self.name} (price: {self.price}, type: {self.type}"
