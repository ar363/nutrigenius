from ninja import NinjaAPI, File, Schema
from ninja.security import HttpBearer
from django.http import HttpResponse
import os
import jwt
from django.contrib.auth.models import User
from django.conf import settings
from typing import List
from datetime import datetime

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # stop yapping tensorflow
import tensorflow as tf
from ninja.files import UploadedFile
from .ai import us_predictor, ind_predictor
from .models import FoodHistory

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


class PastMealSchema(Schema):
    food: str
    quantity: int
    created_at: datetime


@api.get("/past-meals", auth=auth, response=List[PastMealSchema])
def past_meals(request):
    meals = FoodHistory.objects.filter(user_id=request.auth).order_by("-created_at")
    return meals
