import pytest

# This simulates the data we get from OpenSky
def validate_flight_data(data):
    required_keys = ["callsign", "latitude", "longitude", "altitude"]
    for key in required_keys:
        if key not in data:
            return False
    if not isinstance(data["latitude"], float) or not isinstance(data["longitude"], float):
        return False
    return True

# This is the actual test the robot will run
def test_flight_structure():
    # A sample "Good" flight
    good_flight = {
        "callsign": "AIC101",
        "latitude": 19.07,
        "longitude": 72.87,
        "altitude": 3000.5
    }
    
    # A sample "Bad" flight (missing altitude)
    bad_flight = {
        "callsign": "BAD101",
        "latitude": 19.07,
        "longitude": 72.87
    }

    assert validate_flight_data(good_flight) == True
    assert validate_flight_data(bad_flight) == False