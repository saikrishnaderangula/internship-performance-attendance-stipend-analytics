import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate the main dashboard KPIs from the supplied dataframe.
    """

    total_interns = len(df)

    completed = int(
        (df["Completed"] == "Yes").sum()
    )

    non_completed = total_interns - completed

    completion_rate = (
        completed / total_interns * 100
        if total_interns
        else 0.0
    )

    average_attendance = (
        df["Attendance %"].mean()
        if total_interns
        else 0.0
    )

    median_attendance = (
        df["Attendance %"].median()
        if total_interns
        else 0.0
    )

    average_cgpa = (
        df["CGPA"].mean()
        if total_interns
        else 0.0
    )

    median_cgpa = (
        df["CGPA"].median()
        if total_interns
        else 0.0
    )

    average_stipend = (
        df["Stipend"].mean()
        if total_interns
        else 0.0
    )

    median_stipend = (
        df["Stipend"].median()
        if total_interns
        else 0.0
    )

    minimum_stipend = (
        df["Stipend"].min()
        if total_interns
        else 0.0
    )

    maximum_stipend = (
        df["Stipend"].max()
        if total_interns
        else 0.0
    )

    zero_stipend_count = int(
        (df["Stipend"] == 0).sum()
    )

    zero_stipend_rate = (
        zero_stipend_count / total_interns * 100
        if total_interns
        else 0.0
    )

    average_mentor_meetings = (
        df["Mentor Meetings"].mean()
        if total_interns
        else 0.0
    )

    minimum_attendance = (
        df["Attendance %"].min()
        if total_interns
        else 0.0
    )

    maximum_attendance = (
        df["Attendance %"].max()
        if total_interns
        else 0.0
    )

    minimum_cgpa = (
        df["CGPA"].min()
        if total_interns
        else 0.0
    )

    maximum_cgpa = (
        df["CGPA"].max()
        if total_interns
        else 0.0
    )

    return {
        "total_interns": total_interns,
        "completed": completed,
        "non_completed": non_completed,
        "completion_rate": completion_rate,
        "average_attendance": average_attendance,
        "median_attendance": median_attendance,
        "minimum_attendance": minimum_attendance,
        "maximum_attendance": maximum_attendance,
        "average_cgpa": average_cgpa,
        "median_cgpa": median_cgpa,
        "minimum_cgpa": minimum_cgpa,
        "maximum_cgpa": maximum_cgpa,
        "average_stipend": average_stipend,
        "median_stipend": median_stipend,
        "minimum_stipend": minimum_stipend,
        "maximum_stipend": maximum_stipend,
        "zero_stipend_count": zero_stipend_count,
        "zero_stipend_rate": zero_stipend_rate,
        "average_mentor_meetings": average_mentor_meetings,
    }