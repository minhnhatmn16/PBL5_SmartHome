import os.path
import time
from datetime import datetime

import firebase_admin
from PIL import Image
from firebase_admin import credentials, db, storage
import urllib.request
import cv2
import numpy as np
import FCM_Send as fcm

url = 'http://192.168.0.5/cam-lo.jpg'
# url = 'http://192.168.43.78/cam-lo.jpg'

tokens = ["fUGLukZqRVSaw94qtv_0Gr:APA91bHk6uUCPnSMQc6fLLf5zmy3nzAIbalIJpvzhuDJVhUOppkq_uqnD6hRQ_VCRKQyRplTt3DQbuXYIyzxIEURtaYldcQi5Ewd19_ueThYuyZTmyiLsCA7N3KYm00vdqvG1XX78f-r"]

# Recognition
recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read('trainer/trainer.yml')
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX
minW = 0.1 * 1024
minH = 0.1 * 768

# Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {'storageBucket': 'smarthome-6ad5a.appspot.com',
                               'databaseURL': 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})
bucket = storage.bucket()
ref_video = db.reference('change_video')
ref_door = db.reference('door')
ref_unknown = db.reference('unknown')


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
        get_video(s[4:])
        return 0, ""
    if s == 'TRAIN_DATA':
        return 1, ""
    return 0, ""


val = 0
face_id = ""
door_open = 0

def handle_change_video(event):
    global val, face_id
    val, face_id = check(event.data)
def handle_change_door(event):
    global door_open
    door_open = event.data

ref_video.listen(handle_change_video)
ref_door.listen(handle_change_door)


def get_video(temp_face_id):
    ref_video.set('')
    blob = bucket.blob("video/" + temp_face_id)
    print("Downloading video ...")
    blob.download_to_filename("video_train/" + temp_face_id + ".mp4")
    while not os.path.exists("video_train/" + temp_face_id + ".mp4"):
        print(".")
    print("Download video successfully")
    add_faceid(temp_face_id)

def add_faceid(temp_face_id):
    while not os.path.exists("video_train/" + temp_face_id + ".mp4"):
        print(".")
    print("Get faceid ...")
    video_path = 'video_train/' + temp_face_id + ".mp4"
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
            cv2.imwrite("dataset/" + temp_face_id + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        if (cv2.waitKey(delay) & 0xFF == 27) or (count >= 60):
            break
    print("Get faceid successfully")
    fcm.sendPush("Add FaceID", "Add FaceID successfully", tokens)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[0].split("_")[1][6:15])
        faces = faceCascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)
    return faceSamples, ids
def traindata():
    print("Trainning ...")
    faces_, ids = getImagesAndLabels(path)
    recognizer.train(faces_, np.array(ids))

    recognizer.write('trainer/trainer.yml')
    print("Train successfully")
    fcm.sendPush("Train data", "Train data successfully", tokens)
    ref_video.set("")

count_unknown = 0
last_time = 0
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
            if door_open == 0:
                if confidence < 100:
                    current_date_time = datetime.now()
                    date = current_date_time.strftime(date_format)
                    ref_his = db.reference('history')
                    ref_his.update({date: get_name(path, id)})
                    ref_door.set(1)
                    door_open = 1
                    count_unknown = 0
                else:
                    count_unknown += 1
                    print(count_unknown)
                    temp_time = time.time()
                    if count_unknown >= 15 and temp_time-last_time >= 10:
                        fcm.sendPush("Security Alert", "Unidentified Person Detected", tokens)

                        last_time = temp_time
                        current_date_time = datetime.now()
                        date = current_date_time.strftime(date_format)
                        ref_his = db.reference('history')
                        name_img = date + ".jpg"

                        file_path = "history/" + name_img

                        cv2.imwrite(file_path, img)
                        while not os.path.exists(file_path):
                            print(".")

                        bucket = storage.bucket()
                        blob = bucket.blob(file_path)
                        blob.upload_from_filename(file_path)
                        print("Uploaded image unknown successfully!")

                        count_unknown = 0
                        ref_his.update({date: "Unknown~123456789"})
                    id = "Unknown"
            else:
                id = ""
                count_unknown = 0


            confidence = " {0}%".format(round(100 - confidence))
            cv2.putText(img, str(id), (x + 10, y), font, 1, (0, 0, 255), 2)
        cv2.imshow('Face Recognition', img)
        k = cv2.waitKey(10) & 0xff
        if (k == 27):
            break
    traindata()
    cv2.destroyAllWindows()

