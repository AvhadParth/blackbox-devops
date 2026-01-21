import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])

consumer = KafkaConsumer(
    'flights',
    bootstrap_servers=['redpanda:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("💾 Recording System Active...")

for message in consumer:
    flight_data = message.value
    
    # Format for Kibana Maps
    flight_data['location'] = {
        "lat": flight_data['latitude'],
        "lon": flight_data['longitude']
    }
    
    # Save to database
    res = es.index(index="flight_radar", body=flight_data)
    print(f"✅ Indexed: {flight_data['callsign']}")