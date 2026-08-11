# This module provides functions for loading and inspecting movie datasets.
from pathlib import Path

import pandas as pd

# Default path to the raw dataset, resolved relative to the project root
# so the loader works regardless of the current working directory.
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "movies.csv"


def load_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the movies dataset from a CSV file.

    Args:
        path: Path to the CSV file containing the movies dataset.
            Defaults to ``data/movies.csv`` at the project root.

    Returns:
        A pandas DataFrame containing the raw movies data.

    Raises:
        FileNotFoundError: If no file exists at the given path.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")

    return pd.read_csv(path)


def inspect_data(df: pd.DataFrame) -> None:
    """Print a quick, standard inspection summary of a DataFrame.

    Prints shape, column names, dtypes/info, descriptive statistics,
    and a preview of the first few rows. Used as a first-pass sanity
    check before any cleaning or analysis begins.

    Args:
        df: The DataFrame to inspect.
    """
    # Display the dimensions of the dataset (number of rows and columns)
    print("=" * 60)
    print("SHAPE (rows, columns)")
    print("=" * 60)
    print(df.shape)

    # List all column names in the dataset
    print("\n" + "=" * 60)
    print("COLUMNS")
    print("=" * 60)
    print(list(df.columns))

    print("\n" + "=" * 60)
    print("INFO")
    print("=" * 60)
    df.info()

    print("\n" + "=" * 60)
    print("DESCRIBE (numeric columns)")
    print("=" * 60)
    print(df.describe())

    print("\n" + "=" * 60)
    print("HEAD")
    print("=" * 60)
    print(df.head())

    print("\n" + "=" * 60)
    print("MISSING VALUES PER COLUMN")
    print("=" * 60)
    print(df.isna().sum())

    print("\n" + "=" * 60)
    print("DUPLICATE ROWS")
    print("=" * 60)
    print(f"Duplicate rows found: {df.duplicated().sum()}")
