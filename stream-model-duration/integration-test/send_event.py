import os
import json
import argparse

from azure.eventhub import EventData, EventHubProducerClient

parser = argparse.ArgumentParser()
parser.add_argument("--ride-id", type=int, required=True)
parser.add_argument("--pu", type=int, required=True)
parser.add_argument("--do", type=int, required=True)
parser.add_argument("--distance", type=float, required=True)
args = parser.parse_args()

connection_str = os.getenv("EVENT_HUB_CONNECTION_STR")
eventhub_name = os.getenv("EVENT_HUB_NAME", "ride-input")


if not connection_str:
    raise ValueError("Missing EVENT_HUB_CONNECTION_STR")

payload = {
    "ride_id": args.ride_id,
    "PULocationID": args.pu,
    "DOLocationID": args.do,
    "trip_distance": args.distance,
}

print(f"📤 Sending event to Event Hub: {eventhub_name}")
print("Payload:")
print(json.dumps(payload, indent=2))

producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_str, eventhub_name=eventhub_name
)
with producer:
    batch = producer.create_batch()
    event = EventData(json.dumps(payload))
    event.content_type = "application/json"  # 👈 add this
    batch.add(event)
    producer.send_batch(batch)
    print(f"✅ Sent ride_id={args.ride_id} to Event Hub '{eventhub_name}'")
