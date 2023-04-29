from fastapi import FastAPI
import cv2
from app.cv_model.model import math

app = FastAPI()


@app.get("/")
async def main():
    returnData = await math()
    return returnData


@app.get("/predictions")
async def predictions():
    return ""


@app.post("/predict")
async def predict():
    return ""
