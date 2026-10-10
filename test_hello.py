"""Unit tests for hello.py."""

import io
import unittest
from contextlib import redirect_stdout

from hello import add, main


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self) -> None:
        self.assertEqual(add(2, 3), 5)

    def test_negative_numbers(self) -> None:
        self.assertEqual(add(-4, -6), -10)

    def test_mixed_signs(self) -> None:
        self.assertEqual(add(-2, 7), 5)

    def test_zero(self) -> None:
        self.assertEqual(add(0, 0), 0)

    def test_floats(self) -> None:
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestMain(unittest.TestCase):
    def test_output(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main()
        self.assertEqual(buffer.getvalue(), "Hello, Arijit!\n2 + 3 = 5\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
