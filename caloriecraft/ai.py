import tensorflow as tf
from django.conf import settings
from . import constants
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
from openai import OpenAI
import io


def preprocess_image(image, target_size):
    image = tf.image.resize(
        image,
        [target_size, target_size],
        method=tf.image.ResizeMethod.BILINEAR,
        antialias=True,
    )

    image = tf.expand_dims(image, axis=0)
    image = tf.cast(image, tf.uint8)
    return image


def preprocess_ind_image(raw_image):
    image = Image.open(io.BytesIO(raw_image))
    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)  # Add a batch dimension
    return input_batch


def us_predictor(decoded_image):
    us_model = tf.lite.Interpreter(
        model_path=str(settings.BASE_DIR / "ai-models" / "usfoods.tflite")
    )

    us_model.allocate_tensors()

    image = preprocess_image(decoded_image, 240)

    us_model.set_tensor(us_model.get_input_details()[0]["index"], image)
    us_model.invoke()

    output = us_model.get_tensor(us_model.get_output_details()[0]["index"])

    output = tf.math.softmax(output[0] / 255.0)

    preds = tf.math.top_k(output, k=3).values.numpy()
    preds_top5 = tf.math.top_k(output, k=5).values.numpy()

    coll_output = (
        [
            constants.sorted_us_foods[i]
            for i in (tf.math.top_k(output, k=3).indices.numpy())
        ],
        list(preds / tf.math.reduce_sum(preds_top5)),
        list(preds),
    )

    json_op = []
    for i in range(3):
        json_op.append(
            {
                "name": coll_output[0][i].replace("_", " ").title(),
                "confidence": (float(coll_output[2][i]) * 100) * 100 - 100,
                "food_info": constants.get_us_food_data(coll_output[0][i]),
            }
        )

    return json_op


def load_ind_model():
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(
        model.fc.in_features, 1000
    )  # Adjust to match the original model's output units
    model.load_state_dict(
        torch.load(
            settings.BASE_DIR / "ai-models" / "indianfoods_classification_model.pth",
            weights_only=False,
        )
    )
    model.eval()

    return model


ind_model = load_ind_model()


def ind_predictor(image_path):
    image = preprocess_ind_image(image_path)
    model = ind_model

    with torch.no_grad():
        output = model(image)

    predicted_classes = torch.topk(output, 3)

    predicted_class_names = [
        constants.sorted_indian_foods[i] for i in predicted_classes.indices.tolist()[0]
    ]
    predicted_class_probs = predicted_classes.values.tolist()[0]

    json_op = []
    for i in range(3):
        name = predicted_class_names[i].replace("_", " ").title()
        food_info = constants.get_ind_food_data(name)
        prob = predicted_class_probs[i]
        json_op.append({"name": name, "confidence": prob, "food_info": food_info})

    return json_op


def recipe_ai(message):

    client = OpenAI(
        api_key=settings.OPENAI_API_KEY,
        organization="org-91yq2CPSx8C1LuufNeb0tdWk",
        project="proj_P77Tb9d0K1ij8vdGHV4weSZi",
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional Data Analyst Dietian, you must understand inputted data and give professional advice and consulting. your response must be in JSON",
            },
            {
                "role": "user",
                "content": f"Based on what the nutrition content of the dish/meal that is provided is, rate the choice for a balanced healthy diet\n{message}.",
            },
        ],
        response_format={"type": "json_object"},
    )

    return completion.choices[0].message
