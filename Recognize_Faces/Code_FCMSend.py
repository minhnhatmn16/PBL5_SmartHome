import time
import firebase_admin
from firebase_admin import credentials, messaging, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {'storageBucket': 'smarthome-6ad5a.appspot.com',
                               'databaseURL': 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})
image_url = "https://static.vecteezy.com/system/resources/previews/000/379/751/original/notification-vector-icon.jpg"
tokens = ["fUGLukZqRVSaw94qtv_0Gr:APA91bHk6uUCPnSMQc6fLLf5zmy3nzAIbalIJpvzhuDJVhUOppkq_uqnD6hRQ_VCRKQyRplTt3DQbuXYIyzxIEURtaYldcQi5Ewd19_ueThYuyZTmyiLsCA7N3KYm00vdqvG1XX78f-r"]
sound = "danger"
def sendPush(title, msg, registration_token, dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg,
            # sound=sound,
            # image=image_url
        ),
        data=dataObject,
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print("Successfully " + title)


value_gas = db.reference("gas")
value_unknown = db.reference("unknown")

last_sent_time = 0
gas = 0
unknown = 0
def handle_gas(event):
    global gas
    gas = event.data

def handle_unknown(event):
    global unknown
    unknown = event.data

value_gas.listen(handle_gas)
value_unknown.listen(handle_unknown)
while True:
    if gas == 1:
        temp = time.time()
        if temp - last_sent_time >= 10:
            last_sent_time = temp
            sendPush("Gas Leakage Alert", "There is a gas leakage in your kitchen", tokens)
            print(temp)
    if unknown == 1:
        temp = time.time()
        sendPush("Security Alert", "Unidentified Person Detected", tokens)
        value_unknown.set(0)
        unknown == 0
        print(temp)


