import argparse, os, json, base64
from azure.eventhub import EventHubProducerClient, EventData

parser = argparse.ArgumentParser()
parser.add_argument("--ride-id", type=int, required=True)
parser.add_argument("--pu", type=int, required=True)
parser.add_argument("--do", type=int, required=True)
parser.add_argument("--distance", type=float, required=True)
args = parser.parse_args()

connection_str = os.getenv("EVENT_HUB_CONNECTION")
eventhub_name = os.getenv("EVENT_HUB_NAME", "ride-input")

if not connection_str:
    raise ValueError("Missing EVENT_HUB_CONNECTION")

ride = {
    "ride": {
        "PULocationID": args.pu,
        "DOLocationID": args.do,
        "trip_distance": args.distance
    },
    "ride_id": args.ride_id
}

payload = ride


client = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)
with client:
    batch = client.create_batch()
    batch.add(EventData(json.dumps(payload)))
    client.send_batch(batch)
    print(f"✅ Sent ride_id={args.ride_id} to Event Hub '{eventhub_name}'")
