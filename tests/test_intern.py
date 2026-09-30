from src.analytics.intern import (
    compare_intern_to_dataset,
    get_directory_summary,
    get_intern_profile,
    get_interns_below_attendance,
    search_interns,
)
from src.data.loader import load_dataset


def test_search_by_intern_id():
    df = load_dataset()

    result = search_interns(df, "1")

    assert len(result) > 0
    assert "Intern ID" in result.columns


def test_search_by_name():
    df = load_dataset()

    name = df["Name"].iloc[0]

    result = search_interns(df, name)

    assert len(result) > 0


def test_intern_profile():
    df = load_dataset()

    intern_id = str(df["Intern ID"].iloc[0])

    profile = get_intern_profile(
        df,
        intern_id,
    )

    assert "Intern ID" in profile
    assert "Name" in profile
    assert "Department" in profile
    assert "Attendance %" in profile
    assert "CGPA" in profile
    assert "Stipend" in profile


def test_invalid_intern_profile():
    df = load_dataset()

    try:
        get_intern_profile(
            df,
            "INVALID_ID",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError for invalid Intern ID."
        )


def test_intern_comparison():
    df = load_dataset()

    intern_id = str(df["Intern ID"].iloc[0])

    result = compare_intern_to_dataset(
        df,
        intern_id,
    )

    assert "attendance_difference" in result
    assert "cgpa_difference" in result
    assert "stipend_difference" in result
    assert "mentor_meetings_difference" in result


def test_low_attendance_filter():
    df = load_dataset()

    result = get_interns_below_attendance(
        df,
        threshold=70,
    )

    assert all(
        result["Attendance %"] < 70
    )


def test_directory_summary():
    df = load_dataset()

    result = get_directory_summary(df)

    assert result["total_interns"] == 150
    assert result["completed"] == 115
    assert result["non_completed"] == 35
    assert result["departments"] == 5
    assert result["universities"] == 5
    assert result["modes"] == 3