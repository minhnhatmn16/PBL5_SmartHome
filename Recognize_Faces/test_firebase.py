import firebase_admin
from firebase_admin import db, credentials

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {"databaseURL" : "https://smarthome-6ad5a-default-rtdb.firebaseio.com/"})

ref = db.reference("/door")
while (True):
    print(ref.get())
    sleep(2)
