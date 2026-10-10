"""Unit test: the id column in the data file must be unique."""

import csv
import unittest
from collections import Counter

from data_quality_agent import INPUT_FILE


class TestUniqueId(unittest.TestCase):
    def test_id_is_unique(self) -> None:
        with INPUT_FILE.open(newline="", encoding="utf-8") as f:
            ids = [row["id"].strip() for row in csv.DictReader(f)]

        duplicates = {id_: n for id_, n in Counter(ids).items() if n > 1}
        self.assertFalse(
            duplicates,
            f"Duplicate ids in {INPUT_FILE.name} (id: count): {duplicates}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
