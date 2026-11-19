from pathlib import Path
import sqlite3

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "diabetes_cleaned.csv"
DB_PATH = PROJECT_ROOT / "sql" / "healthcare.db"

TABLE_NAME = "hospital_analysis"

# Columns used in the SQL analysis
COLUMN_TYPES = {
    "encounter_id": "INTEGER",
    "patient_nbr": "INTEGER",
    "age": "TEXT",
    "race": "TEXT",
    "gender": "TEXT",
    "time_in_hospital": "INTEGER",
    "num_medications": "INTEGER",
    "number_inpatient": "INTEGER",
    "number_outpatient": "INTEGER",
    "number_emergency": "INTEGER",
    "num_lab_procedures": "INTEGER",
    "num_procedures": "INTEGER",
    "number_diagnoses": "INTEGER",
    "A1Cresult": "TEXT",
    "max_glu_serum": "TEXT",
    "diabetesMed": "TEXT",
    "readmitted": "TEXT",
    "readmitted_30_days": "INTEGER",
}


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {CSV_PATH}\n"
            "Run 01_data_cleaning.ipynb first."
        )

    print("Loading cleaned healthcare dataset...")
    df = pd.read_csv(CSV_PATH)

    missing_columns = [
        column for column in COLUMN_TYPES
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df = df[list(COLUMN_TYPES)]

    print(f"Loaded {len(df):,} hospital encounters.")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql(
            TABLE_NAME,
            connection,
            if_exists="replace",
            index=False,
            dtype=COLUMN_TYPES,
        )

        result = connection.execute(
            f"""
            SELECT
                COUNT(*),
                SUM(readmitted_30_days),
                ROUND(AVG(readmitted_30_days) * 100, 2)
            FROM {TABLE_NAME}
            """
        ).fetchone()

    print(f"Database created: {DB_PATH}")
    print(f"Total encounters: {result[0]:,}")
    print(f"30-day readmissions: {result[1]:,}")
    print(f"Readmission rate: {result[2]}%")
    print("SQL database setup complete!")


if __name__ == "__main__":
    main()
