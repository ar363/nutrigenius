import tensorflow as tf
from django.conf import settings
from . import constants


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


def us_predictor(decoded_image):
    us_model = tf.lite.Interpreter(
        model_path=str(settings.BASE_DIR / "old" / "models" / "usfoods.tflite")
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
                "top5_confidence": float(tf.squeeze(coll_output[1][i])),
                "total_confidence": float(coll_output[2][i]),
            }
        )

    return json_op


def ind_predictor(decoded_image):
    ind_model = tf.keras.models.load_model(
        str(settings.BASE_DIR / "old" / "models" / "ind_softmax.keras")
    )
    ind_image = preprocess_image(decoded_image, 180)
    ind_pred = ind_model.predict(ind_image)
    ind_names = [
        constants.sorted_indian_foods[i]
        for i in tf.math.top_k(ind_pred, k=3).indices.numpy()[0]
    ]
    ind_probs = [i for i in tf.math.top_k(ind_pred, k=3).values.numpy()[0]]
    ind_probs_top5 = [
        i
        for i in tf.math.top_k(ind_pred, k=3).values.numpy()[0]
        / tf.math.reduce_sum(tf.math.top_k(ind_pred, k=5).values.numpy()[0])
    ]
    json_op = []
    for i in range(3):
        json_op.append(
            {
                "name": ind_names[i].replace("_", " ").title(),
                "top5_confidence": float(tf.squeeze(ind_probs_top5[i])),
                "total_confidence": float(ind_probs[i]),
            }
        )

    return json_op
