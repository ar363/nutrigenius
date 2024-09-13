from django.db import models
from django.contrib.auth.models import User
from .constants import get_us_food_data


class FoodHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.CharField(max_length=100)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.username}: {self.food} - {self.quantity} - {self.created_at}"
        )

    def get_food_data(self):
        us_data = get_us_food_data(self.food)
        if us_data:
            for k, v in us_data.items():
                if type(v) == int or type(v) == float:
                    us_data[k] = v * self.quantity
            return us_data

        return {
            "food": self.food,
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0,
            "vitamins": None,
            "fiber": 0,
            "sodium": 0,
        }
