import cv2
face_id = 'Nhat_7e00c2b2-c413-4e91-9ee2-b1736e3b76bf.mp4'
video_path = 'video_train/' + face_id
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
        cv2.imwrite(f"dataset/User." + face_id + "." + str(count) +".jpg", gray[y:y + h, x:x + w])
    cv2.imshow('image', frame)
    if (cv2.waitKey(delay) & 0xFF == 27) or (count>=60):
        break
print("\n Da lay du lieu thanh cong")
capture.release()
cv2.destroyAllWindows()
