from ninja import NinjaAPI, File
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # stop yapping tensorflow
import tensorflow as tf
from ninja.files import UploadedFile
from .ai import us_predictor, ind_predictor

api = NinjaAPI()


@api.get("/ping")
def ping(request):
    return {"ping": "pong"}


@api.post("/predict-img")
def predict_img(request, file: UploadedFile = File(...)):
    raw_image = file.read()
    image = tf.image.decode_image(raw_image)

    us_ob = us_predictor(image)
    in_ob = ind_predictor(image)

    return {"us": us_ob, "ind": in_ob}
