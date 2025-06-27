from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from kitchen_service.settings import base


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})


class Ingredient(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name


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
        base.AUTH_USER_MODEL,
        related_name="dishes"
    )
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")

    class Meta:
        ordering = ("name", )
        verbose_name_plural = "dishes"

    def __str__(self):
        return f"{self.name} (price: {self.price}, type: {self.type})"
