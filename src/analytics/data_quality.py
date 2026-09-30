import pandas as pd


def quality_summary(df: pd.DataFrame) -> dict:
    missing = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    duplicate_ids = int(
        df["Intern ID"].duplicated().sum()
    )

    completeness = (
        100
        if df.size == 0
        else 100 - (
            missing / df.size * 100
        )
    )

    zero_stipend = int(
        (df["Stipend"] == 0).sum()
    )

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": missing,
        "duplicate_rows": duplicate_rows,
        "duplicate_ids": duplicate_ids,
        "completeness": completeness,
        "zero_stipend": zero_stipend,
    }


def numeric_outliers(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    values = df[column]

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[
        (values < lower)
        | (values > upper)
    ].copy()