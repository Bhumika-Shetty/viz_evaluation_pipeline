"""
Download sample datasets for the visualization evaluation pipeline
"""

import os
import pandas as pd
from pathlib import Path

def download_titanic_dataset():
    """Download the Titanic dataset"""
    print("Downloading Titanic dataset...")

    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Download from seaborn datasets (reliable source)
    try:
        import seaborn as sns
        titanic_df = sns.load_dataset('titanic')

        # Save to CSV
        output_path = data_dir / "titanic.csv"
        titanic_df.to_csv(output_path, index=False)

        print(f"✓ Titanic dataset saved to: {output_path}")
        print(f"  Shape: {titanic_df.shape}")
        print(f"  Columns: {', '.join(titanic_df.columns.tolist())}")

        return True

    except Exception as e:
        print(f"✗ Error downloading Titanic dataset: {e}")
        return False


def verify_dataset():
    """Verify that the dataset was downloaded correctly"""
    data_path = Path("data/titanic.csv")

    if not data_path.exists():
        print("✗ Dataset not found!")
        return False

    try:
        df = pd.read_csv(data_path)
        print(f"\n✓ Dataset verified!")
        print(f"  Rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())

        return True

    except Exception as e:
        print(f"✗ Error reading dataset: {e}")
        return False


def main():
    """Main function"""
    print("="*60)
    print("Dataset Download Script")
    print("="*60)
    print()

    # Download Titanic dataset
    success = download_titanic_dataset()

    if success:
        verify_dataset()
        print("\n✓ All datasets ready!")
    else:
        print("\n✗ Download failed. Please check your internet connection.")


if __name__ == "__main__":
    main()
