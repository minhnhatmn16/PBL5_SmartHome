import os.path
import time
from datetime import datetime

import firebase_admin
from PIL import Image
from firebase_admin import credentials, db, storage
import urllib.request
import cv2
import numpy as np


# url = 'http://192.168.0.7/cam-lo.jpg'
url = 'http://192.168.43.78/cam-lo.jpg'


# Recognition
recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX
minW = 0.1 * 1024
minH = 0.1 * 768
names = ['Minh Nhat', 'Duy Tin', 'Anh Quan', 'Ngoc Anh']

# Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {'storageBucket': 'smarthome-6ad5a.appspot.com',
                               'databaseURL': 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})
bucket = storage.bucket()
ref_change = db.reference('change_video')
temp = 0
# Open door
ref_door = db.reference('door')

date_format = "%y%m%d%H%M%S%f"

path = 'dataset'


def get_name(path, id):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        temp = os.path.split(imagePath)[-1].split(".")[0].split("_")
        get_id = int(temp[1][6:15])

        if (get_id == id):
            return temp[0]


def check(s):
    if s[:3] == 'ADD':
        return 1, s[4:]
    if s[:3] == 'DEL':
        return 2, s[4:]
    return 0, ""


val = 0
face_id = ""
door_open = 0


def handle_change(event):
    global val, face_id
    val, face_id = check(event.data)


def handle_change_door(event):
    global door_open
    door_open = event.data


ref_change.listen(handle_change)
ref_door.listen(handle_change_door)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')

        # id = int(os.path.split(imagePath)[-1].split(".")[1])
        id = int(os.path.split(imagePath)[-1].split(".")[0].split("_")[1][6:15])
        print(id)
        faces = faceCascade.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids


def add_faceid(face_id):
    video_path = 'video_train/' + face_id + ".mp4"
    capture = cv2.VideoCapture(video_path)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    delay = 1
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 10)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            # cv2.imwrite(f"dataset/User." + face_id + "." + str(count) + ".jpg", gray[y:y + h, x:x + w])
            cv2.imwrite("dataset/" + face_id + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        if (cv2.waitKey(delay) & 0xFF == 27) or (count >= 60):
            break
    print("\n Da lay du lieu thanh cong")
    print("\n Dang trainning du lieu...")
    faces_, ids = getImagesAndLabels(path)
    recognizer.train(faces_, np.array(ids))

    recognizer.write('trainer/trainer.yml')
    print('\n OKK')


while True:
    while val == 0:
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
            if confidence < 100 and door_open == 0:
                current_date_time = datetime.now()
                date = current_date_time.strftime(date_format)
                ref_his = db.reference('history')
                ref_his.update({date: get_name(path, id)})
                ref_door.set(1)
                door_open = 1
            else:
                id = "Unknown"
            confidence = " {0}%".format(round(100 - confidence))
            cv2.putText(img, str(id), (x + 10, y), font, 1, (0, 0, 255), 2)
            # cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        cv2.imshow('Nhan dien khuon mat', img)
        k = cv2.waitKey(10) & 0xff
        if (k == 27):
            break
    cv2.destroyAllWindows()

    downloading_complete = False
    if val == 1:
        temp_face_id = face_id
        blob = bucket.blob("video/" + temp_face_id)
        blob.download_to_filename("video_train/" + temp_face_id + ".mp4")
        while not os.path.exists("video_train/" + temp_face_id + ".mp4"):
            print("Downloading...")
        ref_change.set('')
        print("Add ok")
        add_faceid(temp_face_id)
    elif val == 2:
        val = 0
