import os
import json
import time
import logging

from azure.eventhub import EventData, EventHubProducerClient
from azure.eventhub.exceptions import EventHubError

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables or hardcode for testing
EVENT_HUB_CONNECTION_STR = os.getenv(
    "EVENT_HUB_CONNECTION_STR",
    "Endpoint=sb://<namespace>.servicebus.windows.net/;"
    "SharedAccessKeyName=RootManageSharedAccessKey;"
    "SharedAccessKey=<your_key>",
)
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME", "ride-input")


def send_event(event_payload):
    try:
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
        )

        with producer:
            batch = producer.create_batch()
            batch.add(EventData(json.dumps(event_payload)))
            producer.send_batch(batch)
            logging.info("✅ Sent ride_id: %s", event_payload.get("ride_id"))

    except EventHubError as eh_err:
        logging.error("❌ Event Hub error: %s", eh_err)
    except ValueError as ve:
        logging.error(
            "❌ Value error during payload preparation: %s", ve, exc_info=True
        )
    except TypeError as te:
        logging.error("❌ Type error during payload formatting: %s", te)


def main():
    try:
        with open("payload.json", encoding="utf-8") as f:
            payloads = json.load(f)

        logging.info("Loaded %d payloads.", len(payloads))
    except FileNotFoundError:
        logging.error("❌ File not found: payload.json")
        return
    except json.JSONDecodeError as jde:
        logging.error("❌ Invalid JSON format in payload.json: %s", jde)
        return
    except OSError as os_err:
        logging.error("❌ OS error during file read: %s", os_err)
        return

    for i, payload in enumerate(payloads):
        logging.info("📤 Sending event %d/%d...", i + 1, len(payloads))
        send_event(payload)
        time.sleep(1)  # simulate streaming rate


if __name__ == "__main__":
    main()
