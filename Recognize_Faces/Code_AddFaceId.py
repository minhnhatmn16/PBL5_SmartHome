from datetime import datetime
from PIL import Image
import numpy as np
import cv2
import os

cam = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer.create()
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

name_face = input('\n Nhập tên: ')

print('\n Khoi tao Camera...')
count = 0
date_format = "%y%m%d%H%M%S%f"
current_date_time = datetime.now()
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    date = current_date_time.strftime(date_format)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        cv2.imwrite("dataset/" + str(name_face) + "_" + date + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 60:
        break
print("\n Da lay du lieu thanh cong")
cam.release()
cv2.destroyAllWindows()


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