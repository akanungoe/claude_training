"""Data quality agent: checks a CSV file for null values and writes an error file."""

import argparse
import csv
import sys
from pathlib import Path

NULL_TOKENS = {"", "null", "none", "nan", "na", "n/a"}

# File checked when no path is given on the command line.
INPUT_FILE = Path(__file__).parent / "sample_data.csv"


def is_null(value: str | None) -> bool:
    return value is None or value.strip().lower() in NULL_TOKENS


def check_nulls(input_path: Path, error_path: Path) -> int:
    """Write rows containing nulls to error_path. Returns the number of bad rows."""
    with input_path.open(newline="", encoding="utf-8") as src:
        reader = csv.DictReader(src)
        if not reader.fieldnames:
            raise ValueError(f"{input_path} has no header row")

        error_rows = []
        # Row 1 is the header, so data starts at line 2.
        for line_no, row in enumerate(reader, start=2):
            null_columns = [col for col in reader.fieldnames if is_null(row.get(col))]
            if null_columns:
                error_rows.append(
                    {
                        "line_number": line_no,
                        "null_columns": ";".join(null_columns),
                        **row,
                    }
                )

    if error_rows:
        with error_path.open("w", newline="", encoding="utf-8") as dst:
            writer = csv.DictWriter(
                dst, fieldnames=["line_number", "null_columns", *reader.fieldnames]
            )
            writer.writeheader()
            writer.writerows(error_rows)
    else:
        # Remove a stale error file from a previous failed run.
        error_path.unlink(missing_ok=True)
    return len(error_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a CSV file for null values.")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=INPUT_FILE,
        help=f"CSV file to check (default: {INPUT_FILE.name})",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="error file path (default: <input>_errors.csv)",
    )
    args = parser.parse_args()

    error_path = args.output or args.input.with_name(f"{args.input.stem}_errors.csv")
    bad_rows = check_nulls(args.input, error_path)

    if bad_rows:
        print(f"FAILED: {bad_rows} row(s) with null values. See {error_path}\n")
        print(error_path.read_text(encoding="utf-8"))
        sys.exit(1)
    print(f"PASSED: no null values found in {args.input}")


if __name__ == "__main__":
    main()
