"""
main.py
-------
Entry point for the Movie Ratings Analysis Dashboard project.

Day 1 responsibilities:
    - Load the raw dataset
    - Run an initial inspection (shape, columns, info, describe)

As the project progresses (Day 2 onward), this script will be
extended to call the cleaning, analysis, and visualization modules
in src/.
"""

from src.data_loader import inspect_data, load_data


def main() -> None:
    """Load the raw movies dataset and print an inspection summary."""
    df = load_data()
    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\n")
    inspect_data(df)


if __name__ == "__main__":
    main()
