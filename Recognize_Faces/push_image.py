import os.path
import time
from datetime import datetime

import firebase_admin
from firebase_admin import  credentials, db, storage, firestore


# Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
    {'storageBucket': 'smarthome-6ad5a.appspot.com',
     'databaseURL' : 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})

date_format = "%y%m%d%H%M%S%f"
current_date_time = datetime.now()
date = current_date_time.strftime(date_format)

local_file_path = "history/Tho_102210075.jpg"
remote_file_name = "history/" + date + ".jpg"

bucket = storage.bucket()
blob = bucket.blob(remote_file_name)
blob.upload_from_filename(local_file_path)
print(f"Uploaded {local_file_path} to {remote_file_name} successfully!")