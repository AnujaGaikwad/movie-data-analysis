
from pathlib import Path

from src.analysis import correlation_matrix, summary_kpis
from src.cleaning import clean_data, save_cleaned_data
from src.data_loader import inspect_data, load_data
from src.visualization import generate_all_charts

PROJECT_ROOT = Path(__file__).resolve().parent
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "movies_cleaned.csv"
IMAGES_DIR = PROJECT_ROOT / "images"


def main() -> None:
    """Load, inspect, clean, save, and analyze the movies dataset."""
    # --- Day 1: Load + inspect the raw dataset ---
    df = load_data()
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\n")
    inspect_data(df)

    # ---  Clean the dataset and save the result ---
    print("\n" + "=" * 60)
    print("CLEANING DATASET")
    print("=" * 60)
    cleaned_df = clean_data(df)
    save_cleaned_data(cleaned_df, str(CLEANED_DATA_PATH))

    print("\n" + "=" * 60)
    print("CLEANED DATASET SUMMARY")
    print("=" * 60)
    inspect_data(cleaned_df)

    # --- Exploratory data analysis ---
    print("\n" + "=" * 60)
    print("GENERATING EDA CHARTS")
    print("=" * 60)
    IMAGES_DIR.mkdir(exist_ok=True)
    generate_all_charts(cleaned_df, str(IMAGES_DIR))

    print("\n" + "=" * 60)
    print("SUMMARY KPIs")
    print("=" * 60)
    for key, value in summary_kpis(cleaned_df).items():
        print(f"{key}: {value}")

    print("\n" + "=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)
    print(correlation_matrix(cleaned_df))


if __name__ == "__main__":
    main()