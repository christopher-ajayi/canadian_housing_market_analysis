import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_FILE = RAW_DATA_DIR / "statcan_income_raw.csv"

OUTPUT_FILE = (
    PROCESSED_DATA_DIR /
    "statcan_income_clean.csv"
)


# ---------------------------------------------------------
# Analytical filters
# ---------------------------------------------------------

PROVINCES = [
    "Newfoundland and Labrador",
    "Prince Edward Island",
    "Nova Scotia",
    "New Brunswick",
    "Quebec",
    "Ontario",
    "Manitoba",
    "Saskatchewan",
    "Alberta",
    "British Columbia",
]


INCOME_CONCEPT = "Median after-tax income"

FAMILY_TYPE = (
    "Economic families and persons not in an economic family"
)

UNIT = "2024 constant dollars"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

def load_data():
    """Load raw Statistics Canada income data."""

    df = pd.read_csv(INPUT_FILE)

    return df


# ---------------------------------------------------------
# Filter analytical observations
# ---------------------------------------------------------

def filter_income_data(df):
    """Select the income observations required for analysis."""

    filtered = df[
        (df["Income concept"] == INCOME_CONCEPT)
        & (
            df["Economic family type"]
            == FAMILY_TYPE
        )
        & (df["UOM"] == UNIT)
        & (
            df["GEO"].isin(PROVINCES)
            | (df["GEO"] == "Canada")
        )
    ].copy()

    return filtered


# ---------------------------------------------------------
# Select and rename columns
# ---------------------------------------------------------

def select_columns(df):
    """Select relevant analytical columns."""

    df = df[
        [
            "REF_DATE",
            "GEO",
            "VALUE",
            "STATUS",
        ]
    ].copy()

    df = df.rename(
        columns={
            "REF_DATE": "year",
            "GEO": "region",
            "VALUE": "median_after_tax_income",
            "STATUS": "status",
        }
    )

    return df


# ---------------------------------------------------------
# Data type conversion
# ---------------------------------------------------------

def convert_data_types(df):
    """Convert columns to appropriate data types."""

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    ).astype("Int64")

    df["median_after_tax_income"] = pd.to_numeric(
        df["median_after_tax_income"],
        errors="coerce"
    )

    df["region"] = df["region"].astype("string")

    df["status"] = df["status"].astype("string")

    return df


# ---------------------------------------------------------
# Data validation
# ---------------------------------------------------------

def validate_data(df):
    """Run basic validation checks."""

    print("\n--- Validation ---")

    print(f"Rows: {len(df):,}")
    print(f"Regions: {df['region'].nunique()}")
    print(
        f"Year range: "
        f"{df['year'].min()} - {df['year'].max()}"
    )

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nObservations by region:")
    print(
        df.groupby("region")
        .size()
        .sort_values()
    )

    print("\nStatus distribution:")
    print(df["status"].value_counts(dropna=False))


# ---------------------------------------------------------
# Save processed dataset
# ---------------------------------------------------------

def save_data(df):
    """Save cleaned income data."""

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nSaved cleaned data to:\n"
        f"{OUTPUT_FILE}"
    )


# ---------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------

def main():

    print("Loading Statistics Canada income data...")

    df = load_data()

    print(f"Raw rows: {len(df):,}")

    df = filter_income_data(df)

    df = select_columns(df)

    df = convert_data_types(df)

    validate_data(df)

    save_data(df)


if __name__ == "__main__":
    main()