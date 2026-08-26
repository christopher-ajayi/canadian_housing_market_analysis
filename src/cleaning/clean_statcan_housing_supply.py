import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


INPUT_FILE = (
    RAW_DATA_DIR /
    "statcan_housing_supply_raw.csv"
)

OUTPUT_FILE = (
    PROCESSED_DATA_DIR /
    "statcan_housing_supply_clean.csv"
)


# ---------------------------------------------------------
# Core geography
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


# ---------------------------------------------------------
# Load
# ---------------------------------------------------------

def load_data():

    return pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Filter geography
# ---------------------------------------------------------

def filter_geography(df):

    df = df[
        df["GEO"].isin(PROVINCES)
        | (df["GEO"] == "Canada")
    ].copy()

    return df


# ---------------------------------------------------------
# Select relevant columns
# ---------------------------------------------------------

def select_columns(df):

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
            "REF_DATE": "month",
            "GEO": "region",
            "VALUE": "housing_starts_saar_thousands",
            "STATUS": "status",
        }
    )

    return df


# ---------------------------------------------------------
# Convert date
# ---------------------------------------------------------

def convert_dates(df):

    df["month"] = pd.to_datetime(
        df["month"],
        format="%Y-%m"
    )

    df["year"] = df["month"].dt.year

    return df


# ---------------------------------------------------------
# Convert units
# ---------------------------------------------------------

def convert_units(df):

    # Raw values are in thousands.
    # Convert to actual annualized housing-start units.

    df["housing_starts_saar"] = (
        df["housing_starts_saar_thousands"]
        * 1_000
    )

    return df


# ---------------------------------------------------------
# Create annual indicator
# ---------------------------------------------------------

def create_annual_data(df):

    annual = (
        df
        .groupby(
            ["year", "region"],
            as_index=False
        )
        .agg(
            housing_starts_saar=(
                "housing_starts_saar",
                "mean"
            )
        )
    )

    return annual


# ---------------------------------------------------------
# Population-style growth
# ---------------------------------------------------------

def calculate_growth(df):

    df = df.sort_values(
        ["region", "year"]
    ).copy()

    df["housing_starts_growth_pct"] = (
        df
        .groupby("region")[
            "housing_starts_saar"
        ]
        .pct_change()
        * 100
    )

    return df


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_data(df):

    print("\n--- Validation ---")

    print(
        f"Rows: {len(df):,}"
    )

    print(
        f"Regions: "
        f"{df['region'].nunique()}"
    )

    print(
        f"Year range: "
        f"{df['year'].min()} - "
        f"{df['year'].max()}"
    )

    print("\nMissing values:")

    print(
        df.isna().sum()
    )

    print("\nDuplicates:")

    print(
        df.duplicated(
            subset=["year", "region"]
        ).sum()
    )

    print("\nObservations by region:")

    print(
        df.groupby("region")
        .size()
    )

    print("\nSample:")

    print(
        df.head(15).to_string(
            index=False
        )
    )


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

def save_data(df):

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nSaved cleaned data to:\n"
        f"{OUTPUT_FILE}"
    )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print(
        "Loading Statistics Canada "
        "housing starts data..."
    )

    df = load_data()

    print(
        f"Raw rows: {len(df):,}"
    )

    df = filter_geography(df)

    df = select_columns(df)

    df = convert_dates(df)

    df = convert_units(df)

    df = create_annual_data(df)

    df = calculate_growth(df)

    validate_data(df)

    save_data(df)


if __name__ == "__main__":
    main()