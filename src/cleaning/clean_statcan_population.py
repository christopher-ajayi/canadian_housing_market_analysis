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


# ---------------------------------------------------------
# Files
# ---------------------------------------------------------

INPUT_FILE = (
    RAW_DATA_DIR /
    "statcan_population_raw.csv"
)

OUTPUT_FILE = (
    PROCESSED_DATA_DIR /
    "statcan_population_clean.csv"
)


# ---------------------------------------------------------
# Geography
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
# Load data
# ---------------------------------------------------------

def load_data():

    df = pd.read_csv(INPUT_FILE)

    return df


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
# Select columns
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
            "REF_DATE": "quarter",
            "GEO": "region",
            "VALUE": "population",
            "STATUS": "status",
        }
    )

    return df


# ---------------------------------------------------------
# Convert dates
# ---------------------------------------------------------

def convert_dates(df):

    df["quarter"] = pd.PeriodIndex(
        df["quarter"],
        freq="Q"
    )

    return df


# ---------------------------------------------------------
# Convert types
# ---------------------------------------------------------

def convert_data_types(df):

    df["population"] = pd.to_numeric(
        df["population"],
        errors="coerce"
    )

    df["region"] = df["region"].astype("string")

    df["status"] = df["status"].astype("string")

    return df


# ---------------------------------------------------------
# Create annual population
# ---------------------------------------------------------

def create_annual_population(df):

    annual = (
        df
        .assign(year=df["quarter"].dt.year)
        .sort_values(
            ["region", "quarter"]
        )
        .groupby(
            ["region", "year"],
            as_index=False
        )
        .last()
    )

    annual = annual[
        [
            "year",
            "region",
            "population",
            "status",
        ]
    ]

    return annual


# ---------------------------------------------------------
# Calculate population growth
# ---------------------------------------------------------

def calculate_population_growth(df):

    df = df.sort_values(
        ["region", "year"]
    ).copy()

    df["population_growth_pct"] = (
        df
        .groupby("region")["population"]
        .pct_change()
        * 100
    )

    return df


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

def validate_data(df):

    print("\n--- Validation ---")

    print(f"Rows: {len(df):,}")

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
        "population data..."
    )

    df = load_data()

    print(
        f"Raw rows: {len(df):,}"
    )

    df = filter_geography(df)

    df = select_columns(df)

    df = convert_dates(df)

    df = convert_data_types(df)

    df = create_annual_population(df)

    df = calculate_population_growth(df)

    validate_data(df)

    save_data(df)


if __name__ == "__main__":
    main()