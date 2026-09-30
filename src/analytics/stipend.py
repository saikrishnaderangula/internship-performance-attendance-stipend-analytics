import pandas as pd


def stipend_summary(df: pd.DataFrame) -> dict:
    """Return core stipend statistics."""

    if df.empty:
        return {
            "average": 0.0,
            "median": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "zero_count": 0,
            "zero_rate": 0.0,
        }

    zero_count = int((df["Stipend"] == 0).sum())

    return {
        "average": float(df["Stipend"].mean()),
        "median": float(df["Stipend"].median()),
        "minimum": float(df["Stipend"].min()),
        "maximum": float(df["Stipend"].max()),
        "zero_count": zero_count,
        "zero_rate": zero_count / len(df) * 100,
    }


def stipend_by_group(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Calculate stipend statistics for a grouping column."""

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )

    return (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Average_Stipend=("Stipend", "mean"),
            Median_Stipend=("Stipend", "median"),
            Minimum_Stipend=("Stipend", "min"),
            Maximum_Stipend=("Stipend", "max"),
        )
        .reset_index()
    )


def stipend_distribution(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create descriptive stipend groups."""

    temp = df.copy()

    temp["Stipend Group"] = pd.cut(
        temp["Stipend"],
        bins=[
            -0.01,
            0,
            10000,
            20000,
            30000,
            float("inf"),
        ],
        labels=[
            "0",
            "1–10,000",
            "10,001–20,000",
            "20,001–30,000",
            "30,001+",
        ],
        include_lowest=True,
    )

    return (
        temp.groupby(
            "Stipend Group",
            observed=True,
        )
        .agg(
            Interns=("Intern ID", "count"),
        )
        .reset_index()
    )


def zero_stipend_records(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return all interns with a zero stipend."""

    result = df[
        df["Stipend"] == 0
    ].copy()

    return result.sort_values(
        ["Department", "Intern ID"]
    )


def stipend_vs_attendance(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields required for stipend versus attendance analysis."""

    return df[
        [
            "Intern ID",
            "Name",
            "Attendance %",
            "Stipend",
            "Department",
            "Mode",
            "Completed",
        ]
    ].copy()


def stipend_vs_cgpa(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return fields required for stipend versus CGPA analysis."""

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