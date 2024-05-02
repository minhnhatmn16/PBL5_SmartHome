import time
import firebase_admin
from firebase_admin import credentials, messaging, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {'storageBucket': 'smarthome-6ad5a.appspot.com',
                               'databaseURL': 'https://smarthome-6ad5a-default-rtdb.firebaseio.com/'})
# firebase_admin.initialize_app(cred)
image_url = "https://static.vecteezy.com/system/resources/previews/000/379/751/original/notification-vector-icon.jpg"
tokens = ["deJjYyHTQXiTXUg_0mSSyq:APA91bEmACSXym_nxsB3doh-HlBhDKDWncxFNlh0oRBPCrq4w0kEcdWKraz3lYSY9h1XlNdxQuuRFU-eX0vSqIZpvUfKhaGc6SCsxfqQNwZsD4GZwEc2vAnZ0yJwtHj31Ib6au3GfbIl"]

def sendPush(title, msg, registration_token, dataObject=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg,
            image=image_url
        ),
        data=dataObject,
        tokens=registration_token,
    )
    response = messaging.send_multicast(message)
    print("Successfully ", response)

def handle_gas(event):
    gas = event.data
    if gas > 500:
        sendPush("Hi", "This is a push message", tokens)

value_gas = db.reference("gas")
last_sent_time = 0
gas_greater_than_500 = False

def check_gas(event):
    global last_sent_time, gas_greater_than_500
    gas = event.data
    if gas > 500:
        if not gas_greater_than_500:
            gas_greater_than_500 = True
            last_sent_time = time.time()
            sendPush("Hi", "This is a push message", tokens)
        elif time.time() - last_sent_time >= 5:
            last_sent_time = time.time()
            sendPush("Hi", "This is a push message", tokens)
    else:
        gas_greater_than_500 = False

value_gas.listen(check_gas)

