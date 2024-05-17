import  FCM_Android as fcm

tokens = ["deJjYyHTQXiTXUg_0mSSyq:APA91bEmACSXym_nxsB3doh-HlBhDKDWncxFNlh0oRBPCrq4w0kEcdWKraz3lYSY9h1XlNdxQuuRFU-eX0vSqIZpvUfKhaGc6SCsxfqQNwZsD4GZwEc2vAnZ0yJwtHj31Ib6au3GfbIl"]
fcm.sendPush("Gas Leakage Alert", "There is a gas leakage in your kitchen", tokens)