from ninja import NinjaAPI, File, Schema, Field
from ninja.security import HttpBearer
from django.http import HttpResponse
import os
import jwt
from django.contrib.auth.models import User
from django.conf import settings
from typing import List
from datetime import datetime, timedelta
from django.core.cache import cache

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # stop yapping tensorflow
import tensorflow as tf
from ninja.files import UploadedFile
from .ai import us_predictor, ind_predictor
from .models import FoodHistory, Pantry, get_pantry_str
from fitness_tools.meals.meal_maker import MakeMeal
import google.generativeai as genai

api = NinjaAPI(title="CalorieCraft API", version="1.0.0")


class BearerAuth(HttpBearer):
    def authenticate(self, request, key):
        u = jwt.decode(key, settings.SECRET_KEY, algorithms=["HS256"])
        if u["userid"]:
            return u["userid"]


auth = BearerAuth()


@api.get("/ping")
def ping(request):
    return {"ping": "pong"}


@api.post("/predict-img")
def predict_img(request, file: UploadedFile = File(...)):
    raw_image = file.read()
    image = tf.image.decode_image(raw_image)

    us_ob = us_predictor(image)
    in_ob = ind_predictor(raw_image)
    print(in_ob)

    return {"us": us_ob, "ind": in_ob}


class SignupData(Schema):
    email: str
    password: str


@api.post("/signup")
def signup(request, data: SignupData, response: HttpResponse):

    if User.objects.filter(username=data.email).exists():
        u = User.objects.filter(username=data.email).first()
        correct_pw = u.check_password(data.password)

        if not correct_pw:
            return {"error": "Password is incorrect"}
    else:
        u = User.objects.create_user(data.email, data.email, data.password)

    token = jwt.encode({"userid": u.id}, settings.SECRET_KEY, algorithm="HS256")

    return {"token": token}


class AddFoodData(Schema):
    sel_food: str
    qty: int


@api.post("/add-food", auth=auth)
def add_food(request, data: AddFoodData):

    FoodHistory.objects.create(
        user_id=request.auth,
        food=data.sel_food,
        quantity=data.qty,
    )

    return {"message": "add-food"}


class AddPantryData(Schema):
    name: str
    count: int


@api.post("/add-pantry", auth=auth)
def add_pantry(request, data: List[AddPantryData]):

    for i in data:
        _, created = Pantry.objects.get_or_create(
            name=i.name, user_id=request.auth, defaults={"quantity": i.count}
        )

        if not created:
            pantry = Pantry.objects.get(name=i.name, user_id=request.auth)
            pantry.quantity += i.count
            pantry.save()

    return {"message": "add-food"}


class PastMealSchema(Schema):
    food: str
    quantity: int
    created_at: datetime
    food_data: dict = Field(None, alias="get_food_data")


class PastMealFullSchema(Schema):
    meals: List[PastMealSchema]
    sums: object


@api.get("/past-meals", auth=auth, response=PastMealFullSchema)
def past_meals(request):
    meals = FoodHistory.objects.filter(user_id=request.auth).order_by("-created_at")

    foods = FoodHistory.objects.filter(
        user_id=request.auth, created_at__gte=datetime.now() - timedelta(days=1)
    )

    sums = {
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "calories": 0,
    }

    for food in foods:
        food_data = food.get_food_data()
        sums["protein"] += food_data["protein"]
        sums["fat"] += food_data["fat"]
        sums["carbs"] += food_data["carbs"]
        sums["calories"] += food_data["calories"]

    return {"meals": meals, "sums": sums}


class FitnessToolData(Schema):
    weight: int
    goal: str
    activity_level: str


@api.post("/fitness-tool")
def fitness_tool(request, data: FitnessToolData):
    goal = None
    activity_level = None
    if data.goal in ["weight_loss", "maintenance", "weight_gain"]:
        goal = data.goal

    if data.activity_level in ["sedentary", "moderate", "very"]:
        activity_level = data.activity_level

    meal = MakeMeal(
        goal=goal,
        activity_level=activity_level,
        weight=data.weight,
        carb_percent=None,
        fat_percent=None,
        protein_percent=None,
        body_type="ectomorph",
        min_cal=1300,
        max_cal=2200,
    )

    return meal.daily_requirements()


@api.post("/dietician", auth=auth)
def dietician(request):

    model = genai.GenerativeModel("gemini-1.5-flash")

    foods = FoodHistory.objects.filter(
        user_id=request.auth, created_at__gte=datetime.now() - timedelta(days=1)
    )

    sums = {
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "calories": 0,
    }

    for food in foods:
        food_data = food.get_food_data()
        sums["protein"] += food_data["protein"]
        sums["fat"] += food_data["fat"]
        sums["carbs"] += food_data["carbs"]
        sums["calories"] += food_data["calories"]

    if cache.get(f"advice_{request.auth}"):
        response = cache.get(f"advice_{request.auth}")
        return {"message": response}
    else:
        response = model.generate_content(
            f"You are a smart A.I Professional Dietitian, you must do everythying that a dietitain would {sums['protein']} grams of protein, {sums['fat']} grams of fat, {sums['carbs']} grams of carbs, {sums['calories']} calories is the daily intake of the user. Rate the choice for a balanced healthy diet, recommend changes and ways to improve the diet of the user."
        )

        cache.set(f"advice_{request.auth}", response.text, 60 * 60 * 24)

        return {"message": response.text}


@api.post("/recipegen", auth=auth)
def recipegen(request):

    model = genai.GenerativeModel("gemini-1.5-flash")

    foods = FoodHistory.objects.filter(
        user_id=request.auth, created_at__gte=datetime.now() - timedelta(days=1)
    )

    sums = {
        "protein": 0,
        "fat": 0,
        "carbs": 0,
    }

    for food in foods:
        food_data = food.get_food_data()
        sums["protein"] += food_data["protein"]
        sums["fat"] += food_data["fat"]
        sums["carbs"] += food_data["carbs"]

    if cache.get(f"recipe_{request.auth}"):
        response = cache.get(f"recipe_{request.auth}")
        return {"message": response}
    else:
        response = model.generate_content(
            f"You are a michellin start chef, you must use any or some of the following ingredients to make a dish:\n{get_pantry_str()}\n\nThe user has consumed {sums['protein']} grams of protein, {sums['fat']} grams of fat, {sums['carbs']} grams of carbs today, take that into account to make a recipe that balances their diet."
        )

        cache.set(f"recipe_{request.auth}", response.text, 60 * 10)

        return {"message": response.text}
