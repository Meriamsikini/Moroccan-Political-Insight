import firebase_admin
from firebase_admin import credentials, db
from kafka import KafkaProducer
import json

# Path to your Firebase key (to be filled in privately)
cred = credentials.Certificate(r"")  # <-- Firebase key

# URL of your Firebase database (to be provided privately)
firebase_admin.initialize_app(cred, {
    'databaseURL': ""  # <--  the URL of the Firebase Realtime Database
})

#Kafka Producer (broker address to be entered privately)
producer = KafkaProducer(
    bootstrap_servers='',  # <-- IP address of the VM
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(0, 10)
)

# Read from the Firebase root
ref = db.reference('/')
data = ref.get()

#Sending line by line to Kafka
if isinstance(data, list):
    for item in data:
        producer.send('json-topic', item)
elif isinstance(data, dict):
    for key, val in data.items():
        producer.send('json-topic', val)

producer.flush()
print("✅ Données envoyées à Kafka")
