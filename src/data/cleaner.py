from pathlib import Path

import pandas as pd

from src.data.loader import load_dataset
from src.data.validator import (
    generate_validation_report,
    validate_required_columns,
)


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "internship_cleaned.csv"


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the internship dataset without creating or removing records.

    The original dataset is never modified.
    """

    cleaned = df.copy()

    # Clean surrounding whitespace from text columns.
    text_columns = cleaned.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    # Ensure numeric columns have numeric data types.
    numeric_columns = [
        "Duration (Weeks)",
        "Mentor Meetings",
        "Attendance %",
        "CGPA",
        "Stipend",
    ]

    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="raise",
        )

    # Keep Intern ID as a string identifier.
    cleaned["Intern ID"] = cleaned["Intern ID"].astype("string")

    # Create a descriptive attendance flag.
    # 70% is a configurable dashboard threshold,
    # not an official policy requirement.
    cleaned["Low Attendance"] = (
        cleaned["Attendance %"] < 70
    )

    return cleaned


def save_cleaned_dataset(df: pd.DataFrame) -> Path:
    """Save the cleaned dataset as a CSV file."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        PROCESSED_PATH,
        index=False,
        encoding="utf-8",
    )

    return PROCESSED_PATH


def run_cleaning_pipeline() -> pd.DataFrame:
    """Load, validate, clean and save the dataset."""

    df = load_dataset()

    missing_columns = validate_required_columns(df)

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    validation_report = generate_validation_report(df)

    if validation_report["missing_columns"]:
        raise ValueError(
            f"Missing columns: "
            f"{validation_report['missing_columns']}"
        )

    if validation_report["duplicate_rows"] > 0:
        raise ValueError(
            "Duplicate rows detected. "
            "Review the source data before continuing."
        )

    if validation_report["duplicate_ids"] > 0:
        raise ValueError(
            "Duplicate Intern IDs detected. "
            "Review the source data before continuing."
        )

    if validation_report["completion_drop_inconsistencies"] > 0:
        raise ValueError(
            "Completed/Dropped inconsistencies detected."
        )

    cleaned = clean_dataset(df)

    save_cleaned_dataset(cleaned)

    return cleaned


if __name__ == "__main__":
    cleaned_data = run_cleaning_pipeline()

    print("CLEANING PIPELINE COMPLETED")
    print("=" * 50)
    print(f"Rows: {len(cleaned_data)}")
    print(f"Columns: {len(cleaned_data.columns)}")
    print(f"Output: {PROCESSED_PATH}")

    print("\nCleaned columns:")
    for column in cleaned_data.columns:
        print(f"- {column}")