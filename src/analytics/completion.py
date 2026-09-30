import pandas as pd


def completion_rate(df: pd.DataFrame) -> float:
    """Return the observed completion rate as a percentage."""
    if df.empty:
        return 0.0

    return (
        (df["Completed"] == "Yes").sum()
        / len(df)
        * 100
    )


def completion_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return completed and non-completed counts."""
    completed = int((df["Completed"] == "Yes").sum())
    non_completed = int((df["Completed"] == "No").sum())

    return pd.DataFrame(
        {
            "Status": ["Completed", "Non-Completed"],
            "Count": [completed, non_completed],
        }
    )


def completion_by_group(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Calculate intern count, completed count and observed
    completion rate for a categorical/grouping column.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    result = (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Completed=(
                "Completed",
                lambda values: (values == "Yes").sum(),
            ),
        )
        .reset_index()
    )

    result["Non-Completed"] = (
        result["Interns"] - result["Completed"]
    )

    result["Completion Rate"] = (
        result["Completed"]
        / result["Interns"]
        * 100
    )

    return result


def completion_by_attendance(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate observed completion rate by attendance group."""

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

    result = (
        temp.groupby(
            "Attendance Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
            Completed=(
                "Completed",
                lambda values: (values == "Yes").sum(),
            ),
        )
        .reset_index()
    )

    result["Non-Completed"] = (
        result["Interns"] - result["Completed"]
    )

    result["Completion Rate"] = (
        result["Completed"]
        / result["Interns"]
        * 100
    )

    return result


def completion_by_mentor_meetings(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate observed completion rate by mentor-meeting groups."""

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

    result = (
        temp.groupby(
            "Mentor Meeting Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
            Completed=(
                "Completed",
                lambda values: (values == "Yes").sum(),
            ),
        )
        .reset_index()
    )

    result["Non-Completed"] = (
        result["Interns"] - result["Completed"]
    )

    result["Completion Rate"] = (
        result["Completed"]
        / result["Interns"]
        * 100
    )

    return result


def completion_by_duration(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate observed completion rate by internship duration."""

    return completion_by_group(
        df,
        "Duration (Weeks)",
    )