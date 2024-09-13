import PIL.Image
import torch
from fastapi import FastAPI, UploadFile
import uuid
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="YOLOv5 API")

yolo_model = torch.hub.load("ultralytics/yolov5", "yolov5s")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/yolo5")
def yolo5(image: UploadFile):

    image = PIL.Image.open(image.file)

    results = yolo_model(image)
    rr = results.render()
    yim = PIL.Image.fromarray(rr[0])
    savepath = "frontend/static/media/" + uuid.uuid4().hex + ".jpg"
    yim.save(savepath)
    return {"op": results.pandas().xyxy[0].to_dict(orient="records"), "img": savepath}
