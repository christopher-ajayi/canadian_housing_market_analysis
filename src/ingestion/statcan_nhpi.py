from pathlib import Path
import io
import zipfile

import pandas as pd
import requests


URL = "https://www150.statcan.gc.ca/n1/tbl/csv/18100205-eng.zip"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

OUTPUT_FILE = RAW_DIR / "statcan_nhpi_raw.csv"


def download_nhpi_data():
    print("Downloading Statistics Canada NHPI data...")

    response = requests.get(URL, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        csv_files = [
            name for name in z.namelist()
            if name.lower().endswith(".csv")
            and "metadata" not in name.lower()
        ]

        if not csv_files:
            raise FileNotFoundError("No data CSV found in the downloaded ZIP.")

        print("Files found in ZIP:")
        for file in csv_files:
            print(f"  - {file}")

        data_file = csv_files[0]

        with z.open(data_file) as f:
            df = pd.read_csv(f)

    return df


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    df = download_nhpi_data()

    print(f"\nDownloaded {len(df):,} rows.")
    print(f"Columns: {len(df.columns)}")
    print("Columns:")
    print(df.columns.tolist())

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()