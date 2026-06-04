import paho.mqtt.client as mqtt
import ssl
import json
import time
import pandas as pd

# AWS IoT Configuration
ENDPOINT = "aa3tk9fu9oxdt-ats.iot.ap-south-1.amazonaws.com"
PORT = 8883
TOPIC = "solar/inverter/telemetry"
CLIENT_ID = "inverter-publisher"

# Certificate paths
CERTS_DIR = "src/certs/"
CA_FILE = CERTS_DIR + "AmazonRootCA1.pem"
CERT_FILE = CERTS_DIR + "certificate.pem.crt"
KEY_FILE = CERTS_DIR + "private.pem.key"

# Load processed data
df = pd.read_csv("data/processed_data.csv")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to AWS IoT Core!")
    else:
        print(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published successfully")

# Setup MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_publish = on_publish

# Setup SSL
client.tls_set(
    ca_certs=CA_FILE,
    certfile=CERT_FILE,
    keyfile=KEY_FILE,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

# Connect
client.connect(ENDPOINT, PORT, keepalive=60)
client.loop_start()

time.sleep(2)

# Publish rows one by one
print(f"Publishing {len(df)} readings to AWS IoT Core...")
for i, row in df.iterrows():
    payload = {
        "timestamp": str(row['DATE_TIME']),
        "source_key": row['SOURCE_KEY'],
        "dc_power": row['DC_POWER'],
        "ac_power": row['AC_POWER'],
        "performance_ratio": row['PERFORMANCE_RATIO'],
        "dc_ac_efficiency": row['DC_AC_EFFICIENCY'],
        "anomaly": int(row['ANOMALY'])
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print(f"Row {i+1}: {payload['timestamp']} | Anomaly: {payload['anomaly']}")
    time.sleep(0.5)  # 0.5 second delay between messages

client.loop_stop()
client.disconnect()
print("Done!")