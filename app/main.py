from fastapi import FastAPI
import cv2
from contextlib import asynccontextmanager
from app.services.modelService import predictImage
from app.services.gcpService import uploadImage, getImage
from pydantic import BaseModel


class RequestBody(BaseModel):
    imageUrl: str
    imageId: str


cv_model = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    cv_model["classifier"] = cv2.CascadeClassifier(
        "app/resources/training.xml")
    yield
    # Clean up the ML models and release the resources
    cv_model.clear()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def main():
    return {"message": "pong"}


@app.post("/predict/")
async def predict(request: RequestBody):
    print("predicting image id: test1234")
    prediction = await predictImage(request.imageUrl, cv_model["classifier"], request.imageId)

    print("uploading predicted image...")
    toUpload = await uploadImage(prediction["imageStream"], "test1234")

    print("getting image public url")
    servingUrl = await getImage("test1234")
    return {"prediction": prediction["totalCounted"], "url": servingUrl}
