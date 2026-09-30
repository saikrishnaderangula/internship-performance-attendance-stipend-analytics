from src.analytics.stipend import (
    stipend_by_group,
    stipend_distribution,
    stipend_summary,
    stipend_vs_attendance,
    stipend_vs_cgpa,
    zero_stipend_records,
)
from src.data.loader import load_dataset


def test_stipend_summary():
    df = load_dataset()

    result = stipend_summary(df)

    assert round(result["average"], 0) == 14533
    assert result["median"] == 15000
    assert result["minimum"] == 0
    assert result["maximum"] == 30000
    assert result["zero_count"] == 23
    assert round(result["zero_rate"], 2) == 15.33


def test_stipend_by_department():
    df = load_dataset()

    result = stipend_by_group(
        df,
        "Department",
    )

    assert len(result) == 5
    assert "Average_Stipend" in result.columns
    assert "Median_Stipend" in result.columns


def test_stipend_by_mode():
    df = load_dataset()

    result = stipend_by_group(
        df,
        "Mode",
    )

    assert len(result) == 3
    assert "Average_Stipend" in result.columns


def test_stipend_distribution():
    df = load_dataset()

    result = stipend_distribution(df)

    assert "Stipend Group" in result.columns
    assert "Interns" in result.columns


def test_zero_stipend_records():
    df = load_dataset()

    result = zero_stipend_records(df)

    assert len(result) == 23
    assert (result["Stipend"] == 0).all()


def test_stipend_vs_attendance():
    df = load_dataset()

    result = stipend_vs_attendance(df)

    assert len(result) == 150
    assert "Attendance %" in result.columns
    assert "Stipend" in result.columns


def test_stipend_vs_cgpa():
    df = load_dataset()

    result = stipend_vs_cgpa(df)

    assert len(result) == 150
    assert "CGPA" in result.columns
    assert "Stipend" in result.columns