import requests
import zipfile
import io
import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# Statistics Canada table
TABLE_ID = "11100190"

DOWNLOAD_URL = (
    f"https://www150.statcan.gc.ca/n1/tbl/csv/"
    f"{TABLE_ID}-eng.zip"
)


def download_statcan_table():
    """Download the complete Statistics Canada table."""

    print("Downloading Statistics Canada income data...")

    response = requests.get(
        DOWNLOAD_URL,
        timeout=60
    )

    response.raise_for_status()

    return response.content


def extract_csv(zip_content):
    """Extract the CSV files from the downloaded ZIP."""

    with zipfile.ZipFile(io.BytesIO(zip_content)) as z:

        csv_files = [
            name for name in z.namelist()
            if name.lower().endswith(".csv")
        ]

        print("Files found in ZIP:")
        for file in csv_files:
            print(f"  - {file}")

        for file in csv_files:

            if "Metadata" not in file:
                with z.open(file) as f:
                    df = pd.read_csv(f)

                return df

    raise FileNotFoundError(
        "Could not find the Statistics Canada data CSV."
    )


def main():

    zip_content = download_statcan_table()

    df = extract_csv(zip_content)

    output_file = (
        RAW_DATA_DIR /
        "statcan_income_raw.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nDownloaded {len(df):,} rows."
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print(
        f"Saved to: {output_file}"
    )


if __name__ == "__main__":
    main()