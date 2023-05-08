from fastapi import FastAPI, File, UploadFile
from PIL import Image
from google.cloud import storage
import cv2
import numpy as np
import io
import requests


async def predictImage(imageUrl, classifier, imageId):

    imageObj = ProcessImage(requests.get(imageUrl, stream=True).raw)
    carsIdentified = classifier.detectMultiScale(imageObj["closing"], 1.1, 1)

    imageObj["totalCounted"] = 0
    for (x, y, w, h) in carsIdentified:
        cv2.rectangle(imageObj["image_arr"], (x, y),
                      (x+w, y+h), (255, 0, 0), 2)
        imageObj["totalCounted"] += 1

    imageObj["imageStream"] = io.BytesIO()
    impageParsed = Image.fromarray(imageObj["image_arr"])
    impageParsed.save(imageObj["imageStream"], "PNG")
    impageParsed.close()

    return imageObj


def ProcessImage(imageUrl):
    imageObj = dict()
    image = Image.open(
        imageUrl)

    image = image.resize((600, 450))
    imageObj["image_arr"] = np.array(image)

    grey = cv2.cvtColor(imageObj["image_arr"], cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    dilated = cv2.dilate(blur, np.ones((3, 3)))

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    imageObj["closing"] = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    return imageObj
