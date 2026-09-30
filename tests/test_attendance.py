from src.analytics.attendance import (
    attendance_by_completion,
    attendance_by_group,
    attendance_by_mentor_meetings,
    attendance_distribution,
    attendance_summary,
    low_attendance_records,
)
from src.data.loader import load_dataset


def test_attendance_summary():
    df = load_dataset()

    result = attendance_summary(df)

    assert round(result["average"], 2) == 76.17
    assert result["median"] == 75
    assert result["minimum"] == 55
    assert result["maximum"] == 100


def test_attendance_by_department():
    df = load_dataset()

    result = attendance_by_group(
        df,
        "Department",
    )

    assert len(result) == 5
    assert "Average_Attendance" in result.columns
    assert "Median_Attendance" in result.columns


def test_low_attendance_records():
    df = load_dataset()

    result = low_attendance_records(
        df,
        threshold=70,
    )

    assert all(result["Attendance %"] < 70)


def test_attendance_distribution():
    df = load_dataset()

    result = attendance_distribution(df)

    assert "Attendance Group" in result.columns
    assert "Interns" in result.columns


def test_attendance_by_completion():
    df = load_dataset()

    result = attendance_by_completion(df)

    assert len(result) == 2
    assert "Average_Attendance" in result.columns


def test_attendance_by_mentor_meetings():
    df = load_dataset()

    result = attendance_by_mentor_meetings(df)

    assert "Mentor Meeting Group" in result.columns
    assert "Average_Attendance" in result.columns