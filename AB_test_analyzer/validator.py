import csv


class DataValidator:
    # Public interface
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.valid_data: list[dict[str, str | int]] = []
        self.errors: list[str] = []

    def validate(self) -> None:
        """
        REQUIRES: self.filepath refers to an existing, readable CSV
                  with required columns.
        MODIFIES: self.valid_data, self.errors
        EFFECTS:  Validates all records in the CSV file.
                  Stores valid records and records validation errors.
                  Excludes all records belonging to duplicate user IDs.
        """
        self.valid_data = []
        self.errors = []

        rows = self._read_csv()
        counts = self._count_users(rows)

        for row in rows:
            user_id = row["user_id"]
            group = row["group"]
            converted = row["converted"]

            if self._has_missing_values(row):
                self.errors.append(f"Missing value: {row}")
            elif not self._is_valid_group(group):
                self.errors.append(f"Invalid group: {row}")
            elif not self._is_valid_conversion(converted):
                self.errors.append(f"Invalid conversion: {row}")
            elif self._is_duplicate(user_id, counts):
                self.errors.append(f"Detected duplicate: {row}")
            else:
                self.valid_data.append({
                    "user_id": user_id,
                    "group": group,
                    "converted": int(converted)
                })

    def get_valid_data(self) -> list[dict[str, str | int]]:
        """Return validated records."""
        return self.valid_data

    def get_errors(self) -> list[str]:
        """Return data quality issues."""
        return self.errors

    # Private helpers
    def _read_csv(self) -> list[dict[str, str]]:
        """
        REQUIRES: self.filepath refers to a readable CSV file.
        EFFECTS:  Reads the CSV file and returns a list of dictionaries.
        """
        with open(self.filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _has_missing_values(self, row: dict[str, str]) -> bool:
        """
        EFFECTS: Returns True if any required field is missing.
        """
        return any(
            not (row[key] or "").strip()
            for key in ("user_id", "group", "converted")
        )

    def _is_valid_group(self, group: str) -> bool:
        """
        EFFECTS: Returns True if group is "A" or "B".
        """
        return group == "A" or group == "B"

    def _is_valid_conversion(self, converted: str) -> bool:
        """
        EFFECTS: Returns True if converted is "0" or "1".
        """
        return converted in ("0", "1")

    def _count_users(self, rows: list[dict[str, str]]) -> dict[str, int]:
        """
        EFFECTS: Returns a dictionary mapping each nonempty
                user ID to its occurrence count.
        """
        counts = {}

        for row in rows:
            user_id = row["user_id"]

            if not user_id:
                continue

            if user_id in counts:
                counts[user_id] += 1
            else:
                counts[user_id] = 1

        return counts
    
    def _is_duplicate(self, user_id: str, counts: dict[str, int]) -> bool:
        """
        EFFECTS: Returns True if user_id occurs more than once.
        """
        return counts.get(user_id, 0) > 1
