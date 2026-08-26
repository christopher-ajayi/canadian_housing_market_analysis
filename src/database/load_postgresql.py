from pathlib import Path

import pandas as pd
from sqlalchemy import text

from database_db_core.connection import get_db_engine


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_table(engine, file_path, table_name):
    """Replace a PostgreSQL table with the current source data."""
    print(f"\nLoading {file_path.name} -> {table_name}")

    df = pd.read_csv(file_path)

    print(f"Rows read: {len(df):,}")

    # Replace pandas NaN with Python None
    df = df.where(pd.notnull(df), None)

    # Clear existing records
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name}"))

    # Load current dataset
    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"Loaded {len(df):,} rows into {table_name}")


def validate_table(engine, table_name):
    """Return the number of rows currently in a PostgreSQL table."""
    with engine.connect() as conn:
        result = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        )
        return result.scalar()


def main():
    engine = get_db_engine()

    print("Connected to PostgreSQL.")
    print(
        engine.url.render_as_string(hide_password=True)
    )

    datasets = [
        (
            PROCESSED_DIR / "statcan_income_clean.csv",
            "income",
        ),
        (
            PROCESSED_DIR / "statcan_population_clean.csv",
            "population",
        ),
        (
            PROCESSED_DIR / "statcan_housing_supply_clean.csv",
            "housing_supply",
        ),
        (
            PROCESSED_DIR / "statcan_nhpi_clean.csv",
            "nhpi",
        ),
        (
            RAW_DIR / "boc_policy_rate_raw.csv",
            "policy_rate",
        ),
    ]

    for file_path, table_name in datasets:
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        load_table(
            engine,
            file_path,
            table_name,
        )

    print("\n--- Database Validation ---")

    for _, table_name in datasets:
        count = validate_table(engine, table_name)
        print(f"{table_name}: {count:,} rows")

    print("\nDatabase loading completed successfully.")


if __name__ == "__main__":
    main()