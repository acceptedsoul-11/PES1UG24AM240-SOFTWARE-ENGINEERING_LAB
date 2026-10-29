
from car_rental_rate import (
    process_rental_fleet,
    check_fleet_telematics,
)


def test_invalid_rental_list():
    try:
        process_rental_fleet("invalid", 10)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_negative_admin_fee():
    try:
        process_rental_fleet([], -1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_unconfirmed_and_confirmed_rentals():
    rentals = [
        {"is_confirmed": False},
        {
            "is_confirmed": True,
            "vehicle_type": "economy",
            "driver_age": 30,
            "days": 1,
            "trip_segments": [100],
        },
    ]
    result = process_rental_fleet(rentals, 10)
    assert result == {"total_revenue": 70.0, "status": "STANDARD"}


def test_zero_and_negative_days():
    rentals = [
        {"is_confirmed": True, "days": 0},
        {"is_confirmed": True, "days": -1},
    ]
    assert process_rental_fleet(rentals, 10)["status"] == "EMPTY_BATCH"


def test_all_vehicle_rate_branches():
    rentals = [
        {"is_confirmed": True, "vehicle_type": "luxury", "days": 1},
        {"is_confirmed": True, "vehicle_type": "suv", "days": 1},
        {"is_confirmed": True, "vehicle_type": "economy", "days": 1},
        {"is_confirmed": True, "vehicle_type": "unknown", "days": 1},
    ]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 270.0, "status": "STANDARD"}


def test_trip_distance_boundaries():
    rentals = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-1, 0, 300, 301],
    }]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 220.4, "status": "STANDARD"}


def test_young_driver_long_trip_breaks_loop():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "economy",
        "driver_age": 20,
        "days": 1,
        "trip_segments": [301, 100],
    }]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 310.0, "status": "STANDARD"}


def test_young_driver_luxury_surcharge():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "luxury",
        "driver_age": 24,
        "days": 2,
        "trip_segments": [],
    }]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 340.0, "status": "STANDARD"}


def test_young_driver_non_luxury_surcharge():
    rentals = [{
        "is_confirmed": True,
        "vehicle_type": "suv",
        "driver_age": 24,
        "days": 2,
        "trip_segments": [],
    }]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 180.0, "status": "STANDARD"}


def test_driver_age_boundaries():
    rentals = [
        {"is_confirmed": True, "driver_age": 21, "days": 1,
         "trip_segments": [301]},
        {"is_confirmed": True, "driver_age": 25, "days": 1,
         "trip_segments": []},
    ]
    result = process_rental_fleet(rentals, 0)
    assert result == {"total_revenue": 220.4, "status": "STANDARD"}


def test_high_risk_audit_and_standard_status():
    risky = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-1, -2, -3, -4, -5],
    }]
    standard = [{
        "is_confirmed": True,
        "driver_age": 30,
        "days": 1,
        "trip_segments": [-1, -2, -3, -4],
    }]
    assert process_rental_fleet(risky, 10)["status"] == "HIGH_RISK_AUDIT"
    assert process_rental_fleet(standard, 10)["status"] == "STANDARD"


def test_telematics_empty_and_safe():
    assert check_fleet_telematics([]) == "NO_DATA"
    assert check_fleet_telematics([[80, 101, 90, 100]]) == "SAFE"


def test_telematics_speeding_streak_resets():
    assert check_fleet_telematics([[101, 90, 101]]) == "SAFE"


def test_telematics_ground_vehicle():
    assert check_fleet_telematics([[101, 102]]) == "GROUND_VEHICLE"


def test_multiple_vehicles_and_empty_logs():
    assert check_fleet_telematics([[], [80, 90], [101, 102]]) == "GROUND_VEHICLE"
