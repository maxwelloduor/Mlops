import os
import json
from functools import partial

from azure.eventhub import EventHubConsumerClient

EVENT_HUB_CONN_STR = os.getenv("EVENT_HUB_CONNECTION_STR")
EVENT_HUB_NAME = "ride-predictions"
CONSUMER_GROUP = "$Default"

if not EVENT_HUB_CONN_STR or not EVENT_HUB_NAME:
    raise EnvironmentError("❌ Missing EVENT_HUB_CONNECTION_STR or event hub name")

print(f"📡 Listening on Event Hub: {EVENT_HUB_NAME}")
print(f"🔐 Using Connection String: {EVENT_HUB_CONN_STR}")
print("🚀 Waiting for events (exit after first valid one)...")

status_tracker = {"received": False}


def validate_payload(payload):
    """Validate that payload contains the expected prediction structure."""
    if not isinstance(payload, dict):
        raise ValueError("Payload is not a dict")

    required_keys = {"model", "version", "prediction"}
    if not required_keys.issubset(payload):
        missing = required_keys - payload.keys()
        raise ValueError(f"Missing required keys: {missing}")

    prediction = payload["prediction"]
    if not isinstance(prediction, dict):
        raise ValueError("prediction must be a dict")

    if not {"ride_id", "ride_duration"}.issubset(prediction):
        missing = {"ride_id", "ride_duration"} - prediction.keys()
        raise ValueError(f"Missing keys in prediction: {missing}")

    if not isinstance(prediction["ride_id"], int):
        raise ValueError("ride_id must be an int")

    if not isinstance(prediction["ride_duration"], (float, int)):
        raise ValueError("ride_duration must be a number")


def on_event(partition_context, event, status_tracker_inner, consumer_client):
    """Handle incoming Event Hub messages."""
    if event is None:
        print(f"⚠️ No event received from partition '{partition_context.partition_id}'")
        return

    body = event.body_as_str()
    print("📎 Event object received.")
    print("📦 Raw event body:", body)

    try:
        payload = json.loads(body)
        validate_payload(payload)
        print("✅ Payload structure and values are as expected")

        ride_id = payload["prediction"]["ride_id"]
        ride_duration = payload["prediction"]["ride_duration"]
        print(f"🔮 Prediction for ride_id {ride_id}: {ride_duration} minutes")

        status_tracker_inner["received"] = True
        partition_context.update_checkpoint(event)

        print("🛑 Got our prediction; closing the consumer.")
        consumer_client.close()

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"❌ Error processing event: {exc}")
        partition_context.update_checkpoint(event)


def on_error(_partition_context, error):
    """Handle errors during event consumption."""
    del _partition_context  # acknowledge unused parameter
    print("⚠️ Error in consumer:", error)


def main():
    """Main entrypoint for the test consumer."""
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str=EVENT_HUB_CONN_STR,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENT_HUB_NAME,
        retry_total=3,
        on_error=on_error,
    )

    try:
        consumer.receive(
            on_event=partial(
                on_event, status_tracker_inner=status_tracker, consumer_client=consumer
            ),
            starting_position="@latest",
            owner_level="1",
            max_wait_time=30,
        )
        if status_tracker["received"]:
            print("✅ Event consumed. Exiting integration test.")
        else:
            print("❌ No valid event received within timeout.")
            raise RuntimeError("No valid event received")
    except KeyboardInterrupt:
        print("👋 Interrupted by user")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
