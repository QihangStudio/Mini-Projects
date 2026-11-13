from validator import DataValidator


def test_invalid_data():
    validator = DataValidator("test_validator_invalid.csv")
    validator.validate()

    valid_data = validator.get_valid_data()
    errors = validator.get_errors()

    assert valid_data == [
        {"user_id": "U002", "group": "B", "converted": 0}
    ]

    assert len(errors) == 6

    assert sum("Missing value" in e for e in errors) == 2
    assert sum("Detected duplicate" in e for e in errors) == 2
    assert sum("Invalid group" in e for e in errors) == 1
    assert sum("Invalid conversion" in e for e in errors) == 1


if __name__ == "__main__":
    test_invalid_data()
    print("All tests passed!")
