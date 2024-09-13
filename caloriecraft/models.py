from django.db import models
from django.contrib.auth.models import User


class FoodHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.CharField(max_length=100)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username}: {self.food} - {self.quantity} - {self.created_at}"
        )
