from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class CaloriesTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food = models.CharField(max_length=100)
    calories = models.IntegerField()
    quantity = models.IntegerField()
    protein = models.IntegerField()
    fiber = models.IntegerField()
    carb = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["created", "updated"]

    def __str__(self):
        return self.food