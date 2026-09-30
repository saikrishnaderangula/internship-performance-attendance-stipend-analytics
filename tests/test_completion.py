from src.analytics.completion import (
    completion_by_attendance,
    completion_by_group,
    completion_rate,
    completion_summary,
)
from src.data.loader import load_dataset


def test_completion_rate():
    df = load_dataset()

    result = completion_rate(df)

    assert round(result, 1) == 76.7


def test_completion_summary():
    df = load_dataset()

    result = completion_summary(df)

    assert result.loc[0, "Count"] == 115
    assert result.loc[1, "Count"] == 35


def test_completion_by_department():
    df = load_dataset()

    result = completion_by_group(
        df,
        "Department",
    )

    assert "Department" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Non-Completed" in result.columns
    assert "Completion Rate" in result.columns
    assert len(result) == 5


def test_completion_by_mode():
    df = load_dataset()

    result = completion_by_group(
        df,
        "Mode",
    )

    assert "Mode" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Completion Rate" in result.columns
    assert len(result) == 3


def test_completion_by_university():
    df = load_dataset()

    result = completion_by_group(
        df,
        "University",
    )

    assert "University" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Completion Rate" in result.columns
    assert len(result) == 5


def test_completion_by_gender():
    df = load_dataset()

    result = completion_by_group(
        df,
        "Gender",
    )

    assert "Gender" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Completion Rate" in result.columns
    assert len(result) == 2


def test_completion_by_duration():
    df = load_dataset()

    result = completion_by_group(
        df,
        "Duration (Weeks)",
    )

    assert "Duration (Weeks)" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Completion Rate" in result.columns


def test_completion_by_attendance():
    df = load_dataset()

    result = completion_by_attendance(df)

    assert "Attendance Group" in result.columns
    assert "Interns" in result.columns
    assert "Completed" in result.columns
    assert "Completion Rate" in result.columns


def test_empty_dataset_completion_rate():
    df = load_dataset().iloc[0:0]

    result = completion_rate(df)

    assert result == 0.0