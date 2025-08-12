import os
import json
import base64
import logging

from azure.eventhub import EventHubConsumerClient

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

connection_str = os.getenv("EVENT_HUB_CONNECTION")  # namespace-scoped connection string
eventhub_name = "ride-predictions"  # your output Event Hub


def on_event(partition_context, event):
    raw = event.body_as_str(encoding="UTF-8")
    print("\n📦 Raw event:", raw)

    try:
        # If wrapped in the Kinesis-style structure:
        payload = json.loads(raw)
        encoded = payload.get("kinesis", {}).get("data")
        if encoded:
            decoded = base64.b64decode(encoded).decode("utf-8")
            print("🧠 Decoded:", json.loads(decoded))
        else:
            print("🧠 Direct:", payload)
    except json.JSONDecodeError as jde:

        logging.error("❌ Failed to decode event: %s", jde)
        raise

    partition_context.update_checkpoint(event)


client = EventHubConsumerClient.from_connection_string(
    connection_str,
    consumer_group="$Default",
    eventhub_name=eventhub_name,
)

print("🔍 Listening for predictions on Event Hub...")
with client:
    client.receive(
        on_event=on_event,
        starting_position="-1",  # Start from earliest
    )
