
from pathlib import Path

from src.cleaning import clean_data, save_cleaned_data
from src.data_loader import inspect_data, load_data

# Path where cleaned data will be saved
CLEANED_DATA_PATH = Path(__file__).resolve().parent / "data" / "movies_cleaned.csv"


def main() -> None:
    """Main function to load, inspect, clean, and save movie dataset."""
    # Load the raw dataset
    df = load_data()
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\n")

    # Display initial data inspection summary
    inspect_data(df)

    print("\n" + "=" * 60)
    print("CLEANING DATASET")
    print("=" * 60)

    # Clean the dataset
    cleaned_df = clean_data(df)
    # Save cleaned data to CSV
    save_cleaned_data(cleaned_df, str(CLEANED_DATA_PATH))

    print("\n" + "=" * 60)
    print("CLEANED DATASET SUMMARY")
    print("=" * 60)
    # Display cleaned data inspection summary
    inspect_data(cleaned_df)

if __name__ == "__main__":
    main()
