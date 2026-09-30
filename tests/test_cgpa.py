from src.analytics.cgpa import (
    cgpa_by_completion,
    cgpa_by_group,
    cgpa_distribution,
    cgpa_summary,
    cgpa_vs_attendance,
    cgpa_vs_stipend,
)
from src.data.loader import load_dataset


def test_cgpa_summary():
    df = load_dataset()

    result = cgpa_summary(df)

    assert round(result["average"], 2) == 3.21
    assert round(result["median"], 2) == 3.25
    assert round(result["minimum"], 2) == 2.33
    assert round(result["maximum"], 2) == 4.00


def test_cgpa_by_department():
    df = load_dataset()

    result = cgpa_by_group(
        df,
        "Department",
    )

    assert len(result) == 5
    assert "Average_CGPA" in result.columns
    assert "Median_CGPA" in result.columns


def test_cgpa_by_mode():
    df = load_dataset()

    result = cgpa_by_group(
        df,
        "Mode",
    )

    assert len(result) == 3
    assert "Average_CGPA" in result.columns


def test_cgpa_by_university():
    df = load_dataset()

    result = cgpa_by_group(
        df,
        "University",
    )

    assert len(result) == 5


def test_cgpa_distribution():
    df = load_dataset()

    result = cgpa_distribution(df)

    assert "CGPA Group" in result.columns
    assert "Interns" in result.columns


def test_cgpa_by_completion():
    df = load_dataset()

    result = cgpa_by_completion(df)

    assert len(result) == 2
    assert "Average_CGPA" in result.columns


def test_cgpa_vs_attendance():
    df = load_dataset()

    result = cgpa_vs_attendance(df)

    assert len(result) == 150
    assert "CGPA" in result.columns
    assert "Attendance %" in result.columns


def test_cgpa_vs_stipend():
    df = load_dataset()

    result = cgpa_vs_stipend(df)

    assert len(result) == 150
    assert "CGPA" in result.columns
    assert "Stipend" in result.columns