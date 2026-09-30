import pandas as pd


def attendance_summary(df: pd.DataFrame) -> dict:
    """Return core attendance statistics."""
    if df.empty:
        return {
            "average": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
        }

    return {
        "average": float(df["Attendance %"].mean()),
        "median": float(df["Attendance %"].median()),
        "minimum": float(df["Attendance %"].min()),
        "maximum": float(df["Attendance %"].max()),
    }


def attendance_by_group(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Calculate attendance statistics for a grouping column."""

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    return (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Average_Attendance=("Attendance %", "mean"),
            Median_Attendance=("Attendance %", "median"),
        )
        .reset_index()
    )


def low_attendance_records(
    df: pd.DataFrame,
    threshold: float = 70,
) -> pd.DataFrame:
    """Return interns below the selected attendance threshold."""

    result = df[
        df["Attendance %"] < threshold
    ].copy()

    return result.sort_values(
        "Attendance %"
    )


def attendance_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create descriptive attendance groups."""

    temp = df.copy()

    temp["Attendance Group"] = pd.cut(
        temp["Attendance %"],
        bins=[0, 69.999, 79.999, 89.999, 100],
        labels=[
            "<70%",
            "70–79%",
            "80–89%",
            "90–100%",
        ],
        include_lowest=True,
    )

    return (
        temp.groupby(
            "Attendance Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
        )
        .reset_index()
    )


def attendance_by_completion(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare attendance statistics by completion status."""

    return (
        df.groupby("Completed")
        .agg(
            Interns=("Intern ID", "count"),
            Average_Attendance=("Attendance %", "mean"),
            Median_Attendance=("Attendance %", "median"),
        )
        .reset_index()
    )


def attendance_by_mentor_meetings(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare attendance with mentor-meeting groups."""

    temp = df.copy()

    temp["Mentor Meeting Group"] = pd.cut(
        temp["Mentor Meetings"],
        bins=[0, 2, 4, 6, 8, float("inf")],
        labels=[
            "1–2",
            "3–4",
            "5–6",
            "7–8",
            "9+",
        ],
        include_lowest=True,
    )

    return (
        temp.groupby(
            "Mentor Meeting Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
            Average_Attendance=("Attendance %", "mean"),
        )
        .reset_index()
    )