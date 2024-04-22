# url = 'http://192.168.0.7/cam-lo.jpg'
# url = 'http://192.168.111.172/cam-lo.jpg'
url = 'http://192.168.0.4/cam-lo.jpg'

import urllib.request
import cv2
import numpy as np
import os
import firebase_admin
from firebase_admin import db, credentials

recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {"databaseURL" : "https://smarthome-6ad5a-default-rtdb.firebaseio.com/"})
ref = db.reference("/")
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

names = ['Minh Nhat','Duy Tin','Anh Quan','Ngoc Anh']

# cam = cv2.VideoCapture(0)
# cam.set(3, 640)
# cam.set(4, 480)
#
minW = 0.1 * 1024
minH = 0.1 * 768

while True:
    # ret, img = cam.read()
    resp = urllib.request.urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        if (confidence < 100):

            id = names[id]
            ref.update({"door" : 1})
        else:
            id = "Unknown"

        confidence = " {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 10, y), font, 1, (0, 0, 255), 2)
        # cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    # img = cv2.resize(img, (640,480))
    cv2.imshow('Nhan dien khuon mat', img)

    k = cv2.waitKey(10) & 0xff
    if (k == 27):
        break
print("Thoat")
# cam.release()
cv2.destroyAllWindows()
