
"""
Movie Data Cleaning Pipeline

This module contains functions to clean and preprocess the raw movie dataset.
Each function handles a specific aspect of data cleaning, and they can be
chained together or run independently as needed.
"""

import pandas as pd

# =============================================================================
# Configuration Constants
# =============================================================================

# Maps raw column names from the CSV to standardized snake_case names.
# This ensures consistency and makes column access easier in code.
COLUMN_RENAME_MAP = {
    "Film": "film",
    "Genre": "genre",
    "Lead Studio": "lead_studio",
    "Audience Score %": "audience_score_pct",
    "Profitability": "profitability",
    "Rotten Tomatoes %": "rotten_tomatoes_pct",
    "Worldwide Gross": "worldwide_gross",
    "Year": "year",
}


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename raw column headers to standardized snake_case format.

    This function maps the human-readable column names from the source CSV
    to clean, programmer-friendly column names using the COLUMN_RENAME_MAP.

    Example transformations:
        "Film" -> "film"
        "Lead Studio" -> "lead_studio"
        "Audience Score %" -> "audience_score_pct"

    Args:
        df: Raw DataFrame with original column names from the CSV file.

    Returns:
        DataFrame with columns renamed to snake_case format.

    Note:
        This is typically the first step in the data cleaning pipeline.
    """
    return df.rename(columns=COLUMN_RENAME_MAP)


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate rows from the dataset.

    Duplicate rows can occur when data is collected from multiple sources
    or when records are duplicated during data entry/collection processes.
    Removing duplicates ensures each movie appears only once in the dataset.

    Args:
        df: DataFrame that may contain duplicate identical rows.

    Returns:
        DataFrame with duplicate rows removed and index reset to 0, 1, 2, ...

    Side Effects:
        Prints a message if any duplicates were found and removed.
    """
    before = len(df)
    # Drop all duplicate rows, keeping only the first occurrence
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate row(s).")
    return df


def clean_text_column(series: pd.Series) -> pd.Series:
    """
    Clean text columns by removing whitespace and standardizing to title case.

    Text columns often contain inconsistent formatting - extra spaces, mixed
    case, or inconsistent capitalization. This function normalizes text data
    to a consistent format: stripped whitespace with first letter of each word
    capitalized (title case).

    Example transformations:
        "   NEW YORK   " -> "New York"
        "los angeles" -> "Los Angeles"
        "chicago" -> "Chicago"

    Args:
        series: A pandas Series containing text values that need cleaning.

    Returns:
        A cleaned pandas Series with:
        - All leading/trailing whitespace removed
        - Text converted to title case (first letter of each word capitalized)
        - NA values preserved as-is

    Note:
        This is commonly used on categorical columns like 'genre', 'city', 'country',
        and 'studio_name' to ensure consistent display and matching.
    """
    # Remove leading/trailing whitespace from all text values
    stripped = series.str.strip()
    # Convert to title case: first letter of each word capitalized
    title_cased = stripped.str.title()
    return title_cased


def convert_currency_to_float(series: pd.Series) -> pd.Series:
    """
    Convert a currency-formatted string column to float.

    Handles values like "$115,567,316.00" by stripping the
    currency symbol and thousands separators then converting to numeric.
    Non-convertible values become <NA>.

    Process:
    1. Convert all values to strings (to handle mixed types)
    2. Remove empty strings, NaN, and 'NA' strings
    3. Strip all currency symbols ($) and thousands separators (,)
    4. Convert to numeric type, coercing errors to <NA>

    Example:
        "$115,567,316.00" -> 115567316.0
        "$1.23" -> 1.23
        "N/A" -> <NA>

    Args:
        series: A pandas Series containing currency-formatted strings.

    Returns:
        A pandas Series with converted float values.
        Non-convertible values become <NA>.

    Note:
        This is used for the 'worldwide_gross' column, which often
        contains values like "$1.2 billion".
    """
    # Convert all values to strings first, then strip whitespace
    # and handle special values like empty strings, NaN, and NA
    cleaned = series.astype(str)
    # Remove empty strings, NaN strings, and 'NA' strings
    cleaned = cleaned.replace({'': pd.NA, 'nan': pd.NA, 'NA': pd.NA})
    # Strip currency symbols ($) and thousands separators (,)
    cleaned = cleaned.str.replace(r"[$,]", "", regex=True)
    # Remove any remaining whitespace
    cleaned = cleaned.str.strip()
    # Convert to numeric type, coercing errors to <NA>
    return pd.to_numeric(cleaned, errors="coerce")


def fill_missing_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Fill missing numeric values using the column median.

    Using the median (rather than the mean) reduces the influence of
    outliers, which are common in box-office and rating data.
    The median is more robust for skewed distributions.

    For each specified column:
    1. Ensure the column is numeric (coerce errors to <NA>)
    2. Count missing values
    3. Calculate median of non-missing values
    4. Fill missing values with the median
    5. Print a summary of the imputation

    Args:
        df: DataFrame containing the columns to fill.
        columns: List of numeric column names to fill with median values.

    Returns:
        DataFrame with missing numeric values imputed using column medians.

    Note:
        Columns not found in the DataFrame are skipped silently.
        If a column contains no numeric values after conversion, it's skipped.
    """
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()
    for col in columns:
        # Skip columns that don't exist in the DataFrame
        if col not in df.columns:
            continue
        # Ensure column is numeric for median calculation
        df[col] = pd.to_numeric(df[col], errors="coerce")
        missing_count = int(df[col].isna().sum())
        if missing_count:
            # Calculate median of non-missing values
            median_value = df[col].median()
            if pd.isna(median_value):
                # Nothing numeric to impute (all values are NaN)
                print(f"Column '{col}' contains no numeric values; skipping imputation.")
                continue
            # Fill missing values with the median
            df[col] = df[col].fillna(median_value)
            print(
                f"Filled {missing_count} missing value(s) in '{col}' "
                f"with median ({median_value:.2f})."
            )
    return df


def fill_missing_categorical(
    df: pd.DataFrame, columns: list[str], fill_value: str = "Unknown"
) -> pd.DataFrame:
    """
    Fill missing categorical/text values with a placeholder label.

    Categorical columns (like genre, studio) often have missing values
    that shouldn't be imputed with statistics. Instead, we fill them
    with a consistent placeholder string to maintain data integrity
    and allow filtering/grouping operations.

    Args:
        df: DataFrame containing the columns to fill.
        columns: List of categorical column names to fill.
        fill_value: The placeholder string used to fill missing entries.
                    Default is "Unknown" to clearly indicate missing data.

    Returns:
        DataFrame with missing categorical values filled with the placeholder.

    Example:
        If 'genre' has NaN values, they become "Unknown"
        If 'lead_studio' has NaN values, they become "Unknown"

    Note:
        This approach preserves the ability to filter "Unknown" values
        later if needed, while avoiding NaN issues in grouping/aggregation.
    """
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()
    for col in columns:
        # Count how many missing values exist in this column
        missing_count = df[col].isna().sum()
        if missing_count:
            # Fill all missing values with the specified placeholder
            df[col] = df[col].fillna(fill_value)
            print(f"Filled {missing_count} missing value(s) in '{col}' with '{fill_value}'.")
    return df


def enforce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cast columns to their correct, final data types.

    After cleaning, columns may still be in their original types (often strings).
    This function enforces appropriate pandas data types for each column:
    - Numeric columns become float64 for calculations
    - Year becomes nullable Int64 (preserves missing values)
    - Text columns become pandas 'string' dtype (better NA handling)

    Args:
        df: DataFrame with cleaned but not-yet-typed columns.

    Returns:
        DataFrame with explicit, correct dtypes for every column.

    Type Mapping:
        - year: Int64 (nullable integer, preserves NA)
        - audience_score_pct, rotten_tomatoes_pct: float64
        - profitability: float64
        - worldwide_gross: float64
        - genre, lead_studio, film: string dtype with NA preserved
    """
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Convert 'year' to nullable integer (Int64)
    # This preserves missing values unlike standard int64
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # Convert box office and rating metrics to numeric float types
    # These will be used for calculations, aggregations, and visualizations
    for col in ["audience_score_pct", "rotten_tomatoes_pct", "profitability", "worldwide_gross"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert text columns to pandas 'string' dtype
    # This is better than object dtype for handling NA values properly
    for col in ["genre", "lead_studio", "film"]:
        if col in df.columns:
            df[col] = df[col].astype("string").fillna(pd.NA)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full cleaning pipeline on the raw movies dataset.

    This is the main entry point that chains all cleaning steps together
    in the correct order. Each step builds on the previous ones.

    Pipeline steps (executed in order):
        1. rename_columns()     - Standardize column names to snake_case
        2. clean_text_column()  - Clean 'genre' column text formatting
        3. clean_text_column()  - Clean 'lead_studio' column text (strip only)
        4. convert_currency_to_float() - Convert worldwide_gross from "$1.2M" to float
        5. fill_missing_numeric() - Fill missing rating scores with column medians
        6. fill_missing_categorical() - Fill missing categorical fields with "Unknown"
        7. remove_duplicate_rows() - Remove exact duplicate movie records
        8. enforce_dtypes()     - Cast all columns to their final correct types

    Args:
        df: Raw movies DataFrame, as loaded from data/movies.csv.

    Returns:
        A cleaned, analysis-ready DataFrame with:
        - Standardized column names
        - Cleaned text columns
        - Numeric conversions for currency/ratings
        - No duplicate rows
        - Proper data types for all columns
        - Missing values handled appropriately

    Example Usage:
        >>> from src.data_loader import load_data
        >>> from src.cleaning import clean_data
        >>> raw_df = load_data()
        >>> clean_df = clean_data(raw_df)
        >>> clean_df.head()
    """
    # Step 1: Rename columns to standardized snake_case
    df = rename_columns(df)

    # Step 2: Clean text columns - genre (full title case)
    df["genre"] = clean_text_column(df["genre"])

    # Step 3: Clean lead_studio - only strip whitespace, don't change case
    # (Studio names often have specific capitalization like "Warner Bros")
    df["lead_studio"] = df["lead_studio"].where(
        df["lead_studio"].isna(), df["lead_studio"].str.strip()
    )

    # Step 4: Convert worldwide_gross from currency string to float
    df["worldwide_gross"] = convert_currency_to_float(df["worldwide_gross"])

    # Step 5: Fill missing numeric rating columns with column medians
    df = fill_missing_numeric(df, ["audience_score_pct", "rotten_tomatoes_pct"])

    # Step 6: Fill missing categorical columns with "Unknown" placeholder
    df = fill_missing_categorical(df, ["lead_studio"])

    # Step 7: Remove exact duplicate rows
    df = remove_duplicate_rows(df)

    # Step 8: Enforce final correct data types for all columns
    df = enforce_dtypes(df)

    return df


def save_cleaned_data(df: pd.DataFrame, path: str) -> None:
    """Save the cleaned DataFrame to a CSV file.

    Args:
        df: The cleaned DataFrame to save.
        path: Destination file path for the cleaned CSV.
    """
    df.to_csv(path, index=False)
    print(f"Saved cleaned dataset to: {path}")
