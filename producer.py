import requests
import json
import time
from kafka import KafkaProducer

# Connect to Redpanda
# On Mac, sometimes 'localhost' needs to be explicit
producer = KafkaProducer(
    bootstrap_servers=['redpanda:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# San Francisco Area (Busy airspace, good for testing)
AREA = {'lamin': 37.00, 'lomin': -123.00, 'lamax': 38.00, 'lomax': -121.00}
URL = "https://opensky-network.org/api/states/all"

print("📡 Mac Radar Station Active. Scanning...")

while True:
    try:
        response = requests.get(URL, params=AREA)
        data = response.json()
        
        if 'states' in data and data['states'] is not None:
            for plane in data['states']:
                flight_data = {
                    "timestamp": data['time'],
                    "icao24": plane[0],
                    "callsign": plane[1].strip(),
                    "latitude": plane[6],
                    "longitude": plane[5],
                    "altitude": plane[7],
                    "velocity": plane[9]
                }
                
                # Only send if we have valid location data
                if flight_data['latitude'] and flight_data['longitude']:
                    producer.send('flights', value=flight_data)
                    print(f"✈️  Sent: {flight_data['callsign']}")
        
        else:
            print("No planes found. Waiting...")

        time.sleep(10)

    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(5)