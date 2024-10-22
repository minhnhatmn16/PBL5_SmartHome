from datetime import datetime
from PIL import Image
import numpy as np
import cv2
import os

cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer.create()
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

name_face = input('\n Name: ')

print('\n Init Camera...')
count = 0
date_format = "%y%m%d%H%M%S%f"
current_date_time = datetime.now()
date = current_date_time.strftime(date_format)
folder_name = str(name_face) + "_" + date
os.makedirs(f'dataset/{folder_name}')
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        # cv2.imwrite("dataset/" + str(name_face) + "_" + date + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
        cv2.imwrite("dataset/"+folder_name+"/" + str(name_face) + "_" + date + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 60:
        break
print("\n Get data successfully")
cam.release()
cv2.destroyAllWindows()