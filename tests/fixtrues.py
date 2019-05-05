"""Fixtures."""
import pytest


@pytest.fixture()
def devices_response():
    """Response for devices."""
    return [
        {
            "id": 1,
            "attributes": {},
            "groupId": 0,
            "name": "Custom device1",
            "uniqueId": "111111111",
            "status": "online",
            "lastUpdate": "1970-01-01T00:00:00.000+0000",
            "positionId": 11111,
            "geofenceIds": [1],
            "phone": "",
            "model": "",
            "contact": "",
            "category": "person",
            "disabled": False,
        },
        {
            "id": 2,
            "attributes": {},
            "groupId": 0,
            "name": "Custom device2",
            "uniqueId": "222222222",
            "status": "online",
            "lastUpdate": "1970-01-01T00:00:00.000+0000",
            "positionId": 22222,
            "geofenceIds": [2],
            "phone": "",
            "model": "",
            "contact": "",
            "category": "person",
            "disabled": False,
        },
    ]


@pytest.fixture()
def positions_response():
    """Response for positions."""
    return [
        {
            "id": 11111,
            "attributes": {
                "batteryLevel": 99.0,
                "distance": 0.0,
                "totalDistance": 99.99,
                "motion": False,
            },
            "deviceId": 1,
            "type": None,
            "protocol": "osmand",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "deviceTime": "1970-01-01T00:00:00.000+0000",
            "fixTime": "1970-01-01T00:00:00.000+0000",
            "outdated": False,
            "valid": True,
            "latitude": 00.0000000,
            "longitude": -00.0000000,
            "altitude": 0.0,
            "speed": 0.0,
            "course": 0.0,
            "address": "Cupboard Under the Stairs, 4 Privet Drive, Little Whinging, Surrey.",
            "accuracy": 0.0,
            "network": None,
        },
        {
            "id": 22222,
            "attributes": {
                "batteryLevel": 99.0,
                "distance": 0.0,
                "totalDistance": 99.99,
                "motion": False,
            },
            "deviceId": 2,
            "type": None,
            "protocol": "osmand",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "deviceTime": "1970-01-01T00:00:00.000+0000",
            "fixTime": "1970-01-01T00:00:00.000+0000",
            "outdated": False,
            "valid": True,
            "latitude": 00.0000000,
            "longitude": -00.0000000,
            "altitude": 0.0,
            "speed": 0.0,
            "course": 0.0,
            "address": "Cupboard Under the Stairs, 4 Privet Drive, Little Whinging, Surrey.",
            "accuracy": 0.0,
            "network": None,
        },
    ]


@pytest.fixture()
def geofence_response():
    """Response for events."""
    return [
        {
            "id": 1,
            "attributes": {},
            "calendarId": 0,
            "name": "Home",
            "description": "",
            "area": "POLYGON((00.0000000000, 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000))",
        },
        {
            "id": 2,
            "attributes": {},
            "calendarId": 0,
            "name": "Home",
            "description": "",
            "area": "POLYGON((00.0000000000, 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000, 00.0000000000 00.0000000000))",
        },
    ]


@pytest.fixture()
def event_response():
    """Response for events."""
    return [
        {
            "id": 1,
            "attributes": {},
            "deviceId": 1,
            "type": "deviceOnline",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "positionId": 0,
            "geofenceId": 0,
            "maintenanceId": 0,
        },
        {
            "id": 2,
            "attributes": {},
            "deviceId": 1,
            "type": "deviceMoving",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "positionId": 0,
            "geofenceId": 0,
            "maintenanceId": 0,
        },
        {
            "id": 3,
            "attributes": {},
            "deviceId": 2,
            "type": "deviceStopped",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "positionId": 0,
            "geofenceId": 0,
            "maintenanceId": 0,
        },
        {
            "id": 4,
            "attributes": {},
            "deviceId": 2,
            "type": "deviceUnknown",
            "serverTime": "1970-01-01T00:00:00.000+0000",
            "positionId": 0,
            "geofenceId": 0,
            "maintenanceId": 0,
        },
    ]
