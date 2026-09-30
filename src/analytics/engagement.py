import pandas as pd


def engagement_summary(df: pd.DataFrame) -> dict:
    """Return core mentor-engagement statistics."""

    if df.empty:
        return {
            "average": 0.0,
            "median": 0.0,
            "minimum": 0,
            "maximum": 0,
        }

    return {
        "average": float(df["Mentor Meetings"].mean()),
        "median": float(df["Mentor Meetings"].median()),
        "minimum": int(df["Mentor Meetings"].min()),
        "maximum": int(df["Mentor Meetings"].max()),
    }


def engagement_by_group(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Calculate mentor-meeting statistics by a grouping column."""

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    return (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Average_Mentor_Meetings=(
                "Mentor Meetings",
                "mean",
            ),
            Median_Mentor_Meetings=(
                "Mentor Meetings",
                "median",
            ),
        )
        .reset_index()
    )


def engagement_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create descriptive mentor-meeting groups."""

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
        )
        .reset_index()
    )


def engagement_by_completion(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare mentor meetings by completion status."""

    return (
        df.groupby("Completed")
        .agg(
            Interns=("Intern ID", "count"),
            Average_Mentor_Meetings=(
                "Mentor Meetings",
                "mean",
            ),
            Median_Mentor_Meetings=(
                "Mentor Meetings",
                "median",
            ),
        )
        .reset_index()
    )


def engagement_by_attendance(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare mentor meetings with attendance groups."""

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
            Average_Mentor_Meetings=(
                "Mentor Meetings",
                "mean",
            ),
        )
        .reset_index()
    )


def engagement_vs_cgpa(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields for mentor meetings versus CGPA analysis."""

    return df[
        [
            "Intern ID",
            "Name",
            "Mentor Meetings",
            "CGPA",
            "Attendance %",
            "Completed",
            "Department",
            "Mode",
        ]
    ].copy()


def engagement_vs_stipend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields for mentor meetings versus stipend analysis."""

    return df[
        [
            "Intern ID",
            "Name",
            "Mentor Meetings",
            "Stipend",
            "Attendance %",
            "Completed",
            "Department",
            "Mode",
        ]
    ].copy()