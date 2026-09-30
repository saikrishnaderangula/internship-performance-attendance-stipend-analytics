from src.analytics.attendance import attendance_summary
from src.analytics.cgpa import cgpa_summary
from src.analytics.completion import completion_rate
from src.analytics.engagement import engagement_summary
from src.analytics.intern import get_intern_profile
from src.analytics.kpis import calculate_kpis
from src.analytics.stipend import stipend_summary
from src.data.loader import load_dataset
from src.data.validator import validation_report


def test_dataset():
    df = load_dataset()

    assert len(df) == 150
    assert len(df.columns) == 13
    assert df["Intern ID"].nunique() == 150


def test_kpis():
    df = load_dataset()
    result = calculate_kpis(df)

    assert result["total_interns"] == 150
    assert result["completed"] == 115
    assert round(result["completion_rate"], 1) == 76.7


def test_attendance():
    df = load_dataset()
    result = attendance_summary(df)

    assert round(result["average"], 2) == 76.17
    assert result["median"] == 75


def test_cgpa():
    df = load_dataset()
    result = cgpa_summary(df)

    assert round(result["average"], 2) == 3.21
    assert round(result["median"], 2) == 3.25


def test_stipend():
    df = load_dataset()
    result = stipend_summary(df)

    assert result["zero_count"] == 23
    assert result["median"] == 15000


def test_engagement():
    df = load_dataset()
    result = engagement_summary(df)

    assert round(result["average"], 2) == 5.61


def test_completion():
    df = load_dataset()

    assert round(
        completion_rate(df),
        1,
    ) == 76.7


def test_validation():
    df = load_dataset()
    result = validation_report(df)

    assert result["missing_columns"] == []
    assert result["duplicate_rows"] == 0
    assert result["duplicate_ids"] == 0


def test_intern_profile():
    df = load_dataset()

    intern_id = str(
        df["Intern ID"].iloc[0]
    )

    profile = get_intern_profile(
        df,
        intern_id,
    )

    assert profile["Intern ID"] == df[
        "Intern ID"
    ].iloc[0]