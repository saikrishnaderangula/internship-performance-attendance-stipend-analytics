import pandas as pd


PROFILE_COLUMNS = [
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


def search_interns(
    df: pd.DataFrame,
    query: str = "",
) -> pd.DataFrame:
    """
    Search interns using Intern ID or Name.

    Intern ID is the primary identifier.
    """
    if not query:
        return df.copy()

    query = str(query).strip()

    if not query:
        return df.copy()

    mask = (
        df["Intern ID"]
        .astype(str)
        .str.contains(query, case=False, na=False)
        |
        df["Name"]
        .astype(str)
        .str.contains(query, case=False, na=False)
    )

    return df[mask].copy()


def get_intern_profile(
    df: pd.DataFrame,
    intern_id: str,
) -> dict:
    """Return a selected intern's complete profile."""

    match = df[
        df["Intern ID"].astype(str) == str(intern_id)
    ]

    if match.empty:
        raise ValueError(
            f"Intern ID '{intern_id}' was not found."
        )

    intern = match.iloc[0]

    return {
        column: intern[column]
        for column in PROFILE_COLUMNS
    }


def compare_intern_to_dataset(
    df: pd.DataFrame,
    intern_id: str,
) -> dict:
    """
    Compare an intern's numeric values with the
    corresponding dataset averages.
    """

    match = df[
        df["Intern ID"].astype(str) == str(intern_id)
    ]

    if match.empty:
        raise ValueError(
            f"Intern ID '{intern_id}' was not found."
        )

    intern = match.iloc[0]

    comparisons = {
        "attendance_difference": (
            float(intern["Attendance %"])
            - float(df["Attendance %"].mean())
        ),
        "cgpa_difference": (
            float(intern["CGPA"])
            - float(df["CGPA"].mean())
        ),
        "stipend_difference": (
            float(intern["Stipend"])
            - float(df["Stipend"].mean())
        ),
        "mentor_meetings_difference": (
            float(intern["Mentor Meetings"])
            - float(df["Mentor Meetings"].mean())
        ),
    }

    return comparisons


def get_interns_below_attendance(
    df: pd.DataFrame,
    threshold: float = 70,
) -> pd.DataFrame:
    """Return interns below the selected attendance threshold."""

    return (
        df[
            df["Attendance %"] < threshold
        ]
        .sort_values("Attendance %")
        .copy()
    )


def get_directory_summary(
    df: pd.DataFrame,
) -> dict:
    """Return summary statistics for the intern directory."""

    return {
        "total_interns": len(df),
        "completed": int(
            (df["Completed"] == "Yes").sum()
        ),
        "non_completed": int(
            (df["Completed"] == "No").sum()
        ),
        "departments": int(
            df["Department"].nunique()
        ),
        "universities": int(
            df["University"].nunique()
        ),
        "modes": int(
            df["Mode"].nunique()
        ),
    }