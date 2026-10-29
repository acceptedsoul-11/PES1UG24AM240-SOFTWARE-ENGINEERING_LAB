
import pytest

from car_rental_rate import (
    process_rental_fleet,
    check_fleet_telematics,
)


def test_invalid_rental_inputs():
    with pytest.raises(ValueError):
        process_rental_fleet("invalid", 10)

    with pytest.raises(ValueError):
        process_rental_fleet([], -1)


def test_empty_batch():
    assert process_rental_fleet([], 10) == {
        "total_revenue": 0.0,
        "status": "EMPTY_BATCH",
    }


def test_unconfirmed_rental():
    result = process_rental_fleet(
        [{"is_confirmed": False}], 10
    )
    assert result["status"] == "EMPTY_BATCH"


def test_invalid_rental_days():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": -1},
    ]
    assert process_rental_fleet(rentals, 10)["status"] == "EMPTY_BATCH"


def test_luxury_trip_boundaries():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 24,
        "days": 2,
        "trip_segments": [-1, 300, 301],
    }]
    assert process_rental_fleet(rentals, 10) == {
        "total_revenue": 530.4,
        "status": "STANDARD",
    }


def test_suv_young_driver_long_trip():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "suv",
        "driver_age": 20,
        "days": 1,
        "trip_segments": [301, 100],
    }]
    assert process_rental_fleet(rentals, 0) == {
        "total_revenue": 340.0,
        "status": "STANDARD",
    }


def test_economy_default_values():
    rentals = [{"is_confirmed": True, "trip_segments": [100]}]
    assert process_rental_fleet(rentals, 0) == {
        "total_revenue": 60.0,
        "status": "STANDARD",
    }


def test_high_risk_audit():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-1, -2, -3, -4, -5],
    }]
    assert process_rental_fleet(rentals, 10) == {
        "total_revenue": 50.0,
        "status": "HIGH_RISK_AUDIT",
    }


def test_luxury_young_driver_no_segments():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 18,
        "days": 1,
    }]
    assert process_rental_fleet(rentals, 10) == {
        "total_revenue": 180.0,
        "status": "STANDARD",
    }


def test_telematics_no_data():
    assert check_fleet_telematics([]) == "NO_DATA"


def test_telematics_safe():
    logs = [[80, 110, 90, 105, 100], [70, 80, 101, 95]]
    assert check_fleet_telematics(logs) == "SAFE"


def test_telematics_consecutive_speeding():
    assert check_fleet_telematics([[70, 110, 120]]) == "GROUND_VEHICLE"
