import cv2
import urllib.request
import numpy as np

import os
url = 'http://192.168.0.4/cam-lo.jpg'
# url = 'http://192.168.111.172/cam-lo.jpg'

cam = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n Nhap ID khuon mat: ')
print('\n Khoi tao Camera...')
count = 0

while True:
    # ret, img = cam.read()
    resp = urllib.request.urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 60:
        break
print("\n Da lay du lieu thanh cong")
cam.release()
cv2.destroyAllWindows()
