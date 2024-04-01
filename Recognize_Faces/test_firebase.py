import firebase_admin
from firebase_admin import  credentials, db, storage
import sys

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
    {'storageBucket': 'smarthome-6ad5a.appspot.com',
     'databaseURL' : 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})

bucket = storage.bucket()
ref = db.reference('change_video')

def handle_change(event):
    if (event.data != ""):
        blob = bucket.blob("video/" + event.data)
        blob.download_to_filename("video_train/" + event.data + ".mp4")
        ref.set('')
        print("ok")
ref.listen(handle_change)
