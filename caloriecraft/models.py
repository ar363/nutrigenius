from django.db import models
from django.contrib.auth.models import User
from .constants import get_us_food_data, get_ind_food_data


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
        my_data = get_us_food_data(self.food)
        if not my_data:
            my_data = get_ind_food_data(self.food)

        mod_data = {}

        if my_data:
            for k, v in my_data.items():
                if type(v) == int or type(v) == float:
                    mod_data[k] = v * self.quantity
                else:
                    mod_data[k] = v
            return mod_data

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

    class Meta:
        verbose_name_plural = "Food Histories"


def get_food_hist_str():
    hist = "\n".join(
        [
            f'{i.food} - {i.created_at} - Carbs: {i.get_food_data()["carbs"]}g, Protein: {i.get_food_data()["protein"]}g, Fat: {i.get_food_data()["fat"]}g'
            for i in FoodHistory.objects.all().order_by("-created_at")
        ]
    )
    return hist


class Pantry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.quantity}"

    class Meta:
        verbose_name_plural = "Pantries"
