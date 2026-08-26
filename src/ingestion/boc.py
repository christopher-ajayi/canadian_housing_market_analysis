import requests
import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# Bank of Canada policy interest rate
SERIES_ID = "V39079"

API_URL = (
    f"https://www.bankofcanada.ca/valet/"
    f"observations/{SERIES_ID}/json"
)


def download_boc_policy_rate():
    """Download Bank of Canada policy interest rate data."""

    params = {
        "start_date": "2010-01-01"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def transform_boc_data(data):
    """Convert the Bank of Canada API response into a DataFrame."""

    observations = data["observations"]

    records = []

    for observation in observations:
        records.append({
            "date": observation["d"],
            "policy_rate": observation[SERIES_ID]["v"]
        })

    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(df["date"])
    df["policy_rate"] = pd.to_numeric(df["policy_rate"])

    return df


def main():

    print("Downloading Bank of Canada policy-rate data...")

    data = download_boc_policy_rate()

    df = transform_boc_data(data)

    output_file = RAW_DATA_DIR / "boc_policy_rate_raw.csv"

    df.to_csv(output_file, index=False)

    print(f"Downloaded {len(df):,} observations.")
    print(f"Date range: {df['date'].min().date()} "
          f"to {df['date'].max().date()}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()