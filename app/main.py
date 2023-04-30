from fastapi import FastAPI
import cv2
from app.cv_model.model import predict

app = FastAPI()


@app.get("/")
async def main():
    returnData = await predict("app/test_image/data/testing.jpg")
    return returnData
