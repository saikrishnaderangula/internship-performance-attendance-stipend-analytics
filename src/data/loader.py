from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "Professional_Internship_Dataset_150.xlsx"


def load_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    return pd.read_excel(
        DATA_PATH,
        sheet_name="Internship"
    )


if __name__ == "__main__":
    df = load_dataset()

    print("Dataset loaded successfully")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")