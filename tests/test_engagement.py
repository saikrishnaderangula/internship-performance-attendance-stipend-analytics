from src.analytics.engagement import (
    engagement_by_attendance,
    engagement_by_completion,
    engagement_by_group,
    engagement_distribution,
    engagement_summary,
    engagement_vs_cgpa,
    engagement_vs_stipend,
)
from src.data.loader import load_dataset


def test_engagement_summary():
    df = load_dataset()

    result = engagement_summary(df)

    assert round(result["average"], 2) == 5.61
    assert result["median"] == 6
    assert result["minimum"] == 1
    assert result["maximum"] == 10


def test_engagement_by_department():
    df = load_dataset()

    result = engagement_by_group(
        df,
        "Department",
    )

    assert len(result) == 5
    assert "Average_Mentor_Meetings" in result.columns
    assert "Median_Mentor_Meetings" in result.columns


def test_engagement_by_mode():
    df = load_dataset()

    result = engagement_by_group(
        df,
        "Mode",
    )

    assert len(result) == 3


def test_engagement_distribution():
    df = load_dataset()

    result = engagement_distribution(df)

    assert "Mentor Meeting Group" in result.columns
    assert "Interns" in result.columns


def test_engagement_by_completion():
    df = load_dataset()

    result = engagement_by_completion(df)

    assert len(result) == 2
    assert "Average_Mentor_Meetings" in result.columns


def test_engagement_by_attendance():
    df = load_dataset()

    result = engagement_by_attendance(df)

    assert "Attendance Group" in result.columns
    assert "Average_Mentor_Meetings" in result.columns


def test_engagement_vs_cgpa():
    df = load_dataset()

    result = engagement_vs_cgpa(df)

    assert len(result) == 150
    assert "Mentor Meetings" in result.columns
    assert "CGPA" in result.columns


def test_engagement_vs_stipend():
    df = load_dataset()

    result = engagement_vs_stipend(df)

    assert len(result) == 150
    assert "Mentor Meetings" in result.columns
    assert "Stipend" in result.columns