"""Const for pytraccar."""
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

EVENT_INTERVAL = 30

ATTRIBUTES = {
    "position": {
        "address": "address",
        "latitude": "latitude",
        "longitude": "longitude",
        "accuracy": "accuracy",
        "altitude": "altitude",
        "course": "course",
        "speed": "speed",
    },
    "device": {
        "traccar_id": "id",
        "device_id": "name",
        "updated": "lastUpdate",
        "category": "category",
    },
}
