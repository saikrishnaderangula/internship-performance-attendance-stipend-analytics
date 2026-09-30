from src.analytics.kpis import calculate_kpis
from src.data.loader import load_dataset


def test_calculate_kpis():
    df = load_dataset()

    kpis = calculate_kpis(df)

    assert kpis["total_interns"] == 150
    assert kpis["completed"] == 115
    assert round(kpis["completion_rate"], 1) == 76.7
    assert round(kpis["average_attendance"], 2) == 76.17
    assert round(kpis["average_cgpa"], 2) == 3.21
    assert round(kpis["average_stipend"], 0) == 14533
    assert kpis["zero_stipend_count"] == 23