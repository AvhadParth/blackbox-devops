from elasticsearch import Elasticsearch

# Connect to database
es = Elasticsearch(['http://localhost:9200'])

index_name = "flight_radar"

# 1. Delete the old index (if it exists) to wipe the "bad" mapping
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"🗑️  Deleted old '{index_name}' index.")

# 2. Define the NEW rules (Mapping)
# This tells Elasticsearch: "The 'location' field is strictly a GEO POINT"
mapping = {
    "mappings": {
        "properties": {
            "location": {
                "type": "geo_point"  # <--- The Magic Word
            },
            "timestamp": {
                "type": "date"
            },
            "callsign": {
                "type": "keyword"
            },
            "altitude": {
                "type": "float"
            }
        }
    }
}

# 3. Create the fresh index with the rules
es.indices.create(index=index_name, body=mapping)
print(f"✅ Created new '{index_name}' with correct Geo-Mapping!")