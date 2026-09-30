import pandas as pd


REQUIRED_COLUMNS = [
    "Intern ID",
    "Name",
    "Gender",
    "University",
    "Department",
    "Mode",
    "Completed",
    "Dropped",
    "Duration (Weeks)",
    "Mentor Meetings",
    "Attendance %",
    "CGPA",
    "Stipend",
]


EXPECTED_CATEGORIES = {
    "Gender": {
        "Female",
        "Male",
    },
    "Department": {
        "AI",
        "Data Analytics",
        "HR",
        "Marketing",
        "Web Development",
    },
    "Mode": {
        "Hybrid",
        "Onsite",
        "Remote",
    },
    "Completed": {
        "Yes",
        "No",
    },
    "Dropped": {
        "Yes",
        "No",
    },
}


def validate_required_columns(
    df: pd.DataFrame,
) -> list[str]:
    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]


def missing_values(
    df: pd.DataFrame,
) -> dict[str, int]:
    return {
        column: int(count)
        for column, count in df.isna().sum().items()
    }


def duplicate_rows(
    df: pd.DataFrame,
) -> int:
    return int(df.duplicated().sum())


def duplicate_ids(
    df: pd.DataFrame,
) -> int:
    return int(df["Intern ID"].duplicated().sum())


def invalid_categories(
    df: pd.DataFrame,
) -> dict[str, list[str]]:
    result = {}

    for column, expected_values in EXPECTED_CATEGORIES.items():

        if column not in df.columns:
            continue

        observed_values = set(
            df[column]
            .dropna()
            .unique()
        )

        invalid_values = sorted(
            observed_values - expected_values
        )

        if invalid_values:
            result[column] = invalid_values

    return result


def invalid_numeric_values(
    df: pd.DataFrame,
) -> dict[str, int]:
    checks = {
        "Duration (Weeks)": (
            df["Duration (Weeks)"] <= 0
        ),
        "Mentor Meetings": (
            df["Mentor Meetings"] < 0
        ),
        "Attendance %": (
            (df["Attendance %"] < 0)
            |
            (df["Attendance %"] > 100)
        ),
        "CGPA": (
            (df["CGPA"] < 0)
            |
            (df["CGPA"] > 4)
        ),
        "Stipend": (
            df["Stipend"] < 0
        ),
    }

    result = {}

    for column, condition in checks.items():

        count = int(condition.sum())

        if count > 0:
            result[column] = count

    return result


def completion_drop_inconsistencies(
    df: pd.DataFrame,
) -> int:
    inconsistent = (
        (
            (df["Completed"] == "Yes")
            &
            (df["Dropped"] != "No")
        )
        |
        (
            (df["Completed"] == "No")
            &
            (df["Dropped"] != "Yes")
        )
    )

    return int(inconsistent.sum())


def zero_stipend_count(
    df: pd.DataFrame,
) -> int:
    return int(
        (df["Stipend"] == 0).sum()
    )


def zero_stipend_rate(
    df: pd.DataFrame,
) -> float:
    if df.empty:
        return 0.0

    return (
        zero_stipend_count(df)
        / len(df)
        * 100
    )


def low_attendance_count(
    df: pd.DataFrame,
    threshold: float = 70,
) -> int:
    return int(
        (df["Attendance %"] < threshold).sum()
    )


def validation_report(
    df: pd.DataFrame,
) -> dict:
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_columns": (
            validate_required_columns(df)
        ),
        "missing_values": (
            missing_values(df)
        ),
        "duplicate_rows": (
            duplicate_rows(df)
        ),
        "duplicate_ids": (
            duplicate_ids(df)
        ),
        "invalid_categories": (
            invalid_categories(df)
        ),
        "invalid_numeric_values": (
            invalid_numeric_values(df)
        ),
        "completion_drop_inconsistencies": (
            completion_drop_inconsistencies(df)
        ),
        "zero_stipend_count": (
            zero_stipend_count(df)
        ),
        "zero_stipend_rate": (
            zero_stipend_rate(df)
        ),
        "low_attendance_count": (
            low_attendance_count(df)
        ),
    }


def generate_validation_report(
    df: pd.DataFrame,
) -> dict:
    return validation_report(df)