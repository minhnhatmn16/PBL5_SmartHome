from datetime import datetime

import cv2
import os

cam = cv2.VideoCapture(0)

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# face_id = input('\n Nhap ID khuon mat: ')
name_face = input('\n Nhập tên khuôn mặt : ')

print('\n Khoi tao Camera...')
count = 0
date_format = "%y%m%d%H%M%S%f"
current_date_time = datetime.now()
date = current_date_time.strftime(date_format)
folder_name = str(name_face) + "_" + date
os.makedirs(f'dataset/{folder_name}')
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(int(64), int(48)),
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1
        cv2.imwrite("dataset/"+folder_name+"/" + str(name_face) + "_" + date + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

    cv2.imshow('image', img)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 60:
        break
print("\n Da lay du lieu thanh cong")
cam.release()
cv2.destroyAllWindows()
