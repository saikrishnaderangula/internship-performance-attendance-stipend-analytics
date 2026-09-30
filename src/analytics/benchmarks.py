import pandas as pd


def group_benchmark(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    result = (
        df.groupby(column)
        .agg(
            Interns=("Intern ID", "count"),
            Completion_Rate=(
                "Completed",
                lambda x: (x == "Yes").mean() * 100,
            ),
            Average_Attendance=(
                "Attendance %",
                "mean",
            ),
            Average_CGPA=(
                "CGPA",
                "mean",
            ),
            Average_Stipend=(
                "Stipend",
                "mean",
            ),
            Median_Stipend=(
                "Stipend",
                "median",
            ),
            Average_Mentor_Meetings=(
                "Mentor Meetings",
                "mean",
            ),
        )
        .reset_index()
    )

    return result