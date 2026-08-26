from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "statcan_nhpi_raw.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "statcan_nhpi_clean.csv"
)


PROVINCES = [
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
    "Canada",
]


def load_data():
    print("Loading Statistics Canada NHPI data...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Raw rows: {len(df):,}")

    return df


def clean_data(df):

    # Keep total new housing price index
    df = df[
        df["New housing price indexes"]
        == "Total (house and land)"
    ].copy()

    # Keep Canada and provinces
    df = df[df["GEO"].isin(PROVINCES)].copy()

    # Convert date
    df["date"] = pd.to_datetime(
        df["REF_DATE"],
        format="%Y-%m"
    )

    # Extract year and month
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Rename geography
    df["region"] = df["GEO"]

    # Rename value
    df["nhpi"] = df["VALUE"]

    # Keep relevant columns
    df = df[
        [
            "date",
            "year",
            "month",
            "region",
            "nhpi",
            "STATUS",
        ]
    ].copy()

    # Rename status
    df = df.rename(
        columns={
            "STATUS": "status"
        }
    )

    # Remove observations without an index value
    df = df.dropna(subset=["nhpi"])

    # Sort before calculating growth
    df = df.sort_values(
        ["region", "date"]
    )

    # Monthly NHPI growth
    df["nhpi_growth_pct"] = (
        df.groupby("region")["nhpi"]
        .pct_change()
        * 100
    )

    return df


def validate_data(df):

    print("\n--- Validation ---")

    print(f"Rows: {len(df):,}")
    print(f"Regions: {df['region'].nunique()}")
    print(
        f"Date range: "
        f"{df['date'].min().date()} - "
        f"{df['date'].max().date()}"
    )

    print("\nRegions:")
    print(
        df["region"]
        .drop_duplicates()
        .sort_values()
        .to_string(index=False)
    )

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicates:")
    print(
        df.duplicated(
            subset=["date", "region"]
        ).sum()
    )

    print("\nObservations by region:")
    print(
        df.groupby("region")
        .size()
    )

    print("\nStatus distribution:")
    print(
        df["status"]
        .value_counts(dropna=False)
    )


def main():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = load_data()

    df = clean_data(df)

    validate_data(df)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nSaved cleaned data to:\n"
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()