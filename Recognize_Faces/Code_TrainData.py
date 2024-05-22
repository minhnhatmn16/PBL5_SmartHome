from datetime import datetime
from PIL import Image
import numpy as np
import cv2
import os

cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer.create()
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


path = 'dataset'
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[0].split("_")[1][6:15])
        faces = face_detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids


print("\n Dang trainning du lieu...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('trainer/trainer.yml')
print('\n Train dữ liệu thành công')