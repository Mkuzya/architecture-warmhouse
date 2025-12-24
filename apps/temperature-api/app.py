from flask import Flask, request, jsonify
from datetime import datetime, timezone
import random

app = Flask(__name__)

DEFAULT_LOCATIONS = {
    "1": "Living Room",
    "2": "Bedroom",
    "3": "Kitchen",
}

REVERSE_LOCATIONS = {v: k for k, v in DEFAULT_LOCATIONS.items()}


def resolve_location_and_sensor(location: str, sensor_id: str):
    location = (location or "").strip()
    sensor_id = (sensor_id or "").strip()

    if not location:
        if sensor_id in DEFAULT_LOCATIONS:
            location = DEFAULT_LOCATIONS[sensor_id]
        else:
            location = "Unknown"

    if not sensor_id:
        sensor_id = REVERSE_LOCATIONS.get(location, "0")

    return location, sensor_id


def generate_temperature_payload(location: str, sensor_id: str):
    value = round(random.uniform(19.0, 26.0), 1)
    return {
        "value": value,
        "unit": "C",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "location": location,
        "status": "active",
        "sensor_id": str(sensor_id),
        "sensor_type": "temperature",
        "description": "Simulated temperature reading",
    }


@app.get("/temperature")
def get_temperature_by_location():
    location = request.args.get("location", "")
    sensor_id = request.args.get("sensorId", "")

    location, sensor_id = resolve_location_and_sensor(location, sensor_id)
    payload = generate_temperature_payload(location, sensor_id)
    return jsonify(payload), 200


@app.get("/temperature/<sensor_id>")
def get_temperature_by_id(sensor_id: str):
    location = request.args.get("location", "")

    location, sensor_id = resolve_location_and_sensor(location, sensor_id)
    payload = generate_temperature_payload(location, sensor_id)
    return jsonify(payload), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
