import PIL.Image
import torch
from fastapi import FastAPI, UploadFile
import PIL

app = FastAPI(title="YOLOv5 API")

yolo_model = torch.hub.load("ultralytics/yolov5", "yolov5s")


@app.post("/yolo5")
def yolo5(image: UploadFile):

    image = PIL.Image.open(image.file)

    results = yolo_model(image)
    return results.pandas().xyxy[0].to_dict(orient="records")
