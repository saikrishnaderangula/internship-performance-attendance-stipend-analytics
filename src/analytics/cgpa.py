import pandas as pd


def cgpa_summary(df: pd.DataFrame) -> dict:
    """Return core CGPA statistics."""

    if df.empty:
        return {
            "average": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
        }

    return {
        "average": float(df["CGPA"].mean()),
        "median": float(df["CGPA"].median()),
        "minimum": float(df["CGPA"].min()),
        "maximum": float(df["CGPA"].max()),
    }


def cgpa_by_group(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Calculate CGPA statistics for a grouping column."""

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    return (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Average_CGPA=("CGPA", "mean"),
            Median_CGPA=("CGPA", "median"),
            Minimum_CGPA=("CGPA", "min"),
            Maximum_CGPA=("CGPA", "max"),
        )
        .reset_index()
    )


def cgpa_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create descriptive CGPA groups."""

    temp = df.copy()

    temp["CGPA Group"] = pd.cut(
        temp["CGPA"],
        bins=[
            0,
            2.49,
            2.99,
            3.49,
            4.00,
        ],
        labels=[
            "<2.50",
            "2.50–2.99",
            "3.00–3.49",
            "3.50–4.00",
        ],
        include_lowest=True,
    )

    return (
        temp.groupby(
            "CGPA Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
        )
        .reset_index()
    )


def cgpa_by_completion(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare CGPA statistics by completion status."""

    return (
        df.groupby("Completed")
        .agg(
            Interns=("Intern ID", "count"),
            Average_CGPA=("CGPA", "mean"),
            Median_CGPA=("CGPA", "median"),
        )
        .reset_index()
    )


def cgpa_vs_attendance(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields required for CGPA versus attendance analysis."""

    return df[
        [
            "Intern ID",
            "Name",
            "CGPA",
            "Attendance %",
            "Department",
            "Mode",
            "Completed",
        ]
    ].copy()


def cgpa_vs_stipend(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields required for CGPA versus stipend analysis."""

    return df[
        [
            "Intern ID",
            "Name",
            "CGPA",
            "Stipend",
            "Department",
            "Mode",
            "Completed",
        ]
    ].copy()