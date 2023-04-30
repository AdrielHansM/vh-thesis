from fastapi import FastAPI, File, UploadFile
from PIL import Image
import cv2
import numpy as np
import requests
import os


async def predict(imageUrl):
    imageObj = await ProcessImage(imageUrl)
    car_cascade = await prepareModel()
    cars = car_cascade.detectMultiScale(imageObj["closing"], 1.1, 1)

    totalCounted = 0
    for (x, y, w, h) in cars:
        cv2.rectangle(imageObj["image_arr"], (x, y),
                      (x+w, y+h), (255, 0, 0), 2)
        totalCounted += 1

    Image.fromarray(imageObj["image_arr"]).save(
        "app/test_image/predictions/predicted.png", "PNG")
    return totalCounted


async def ProcessImage(imageUrl):

    imageObj = dict()
    image = Image.open(
        imageUrl)

    image = image.resize((450, 250))
    imageObj["image_arr"] = np.array(image)

    grey = cv2.cvtColor(imageObj["image_arr"], cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    dilated = cv2.dilate(blur, np.ones((3, 3)))

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    imageObj["closing"] = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    return imageObj


async def prepareModel():
    fileXml = open("app/cv_model/car_models.xml")
    car_cascade = cv2.CascadeClassifier("app/cv_model/car_models.xml")
    return car_cascade
