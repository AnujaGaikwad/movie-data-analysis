
import pandas as pd

# Maps raw, human-readable column names to clean snake_case names.
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
    """Rename raw columns to clean, consistent snake_case names.

    Args:
        df: Raw DataFrame with original column names.

    Returns:
        DataFrame with renamed columns.
    """
    return df.rename(columns=COLUMN_RENAME_MAP)


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows from the dataset.

    Args:
        df: DataFrame that may contain duplicate rows.

    Returns:
        DataFrame with duplicate rows removed, index reset.
    """
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate row(s).")
    return df


def clean_text_column(series: pd.Series) -> pd.Series:
    """Strip whitespace and standardize casing for a text column.

    Args:
        series: A pandas Series containing text values.

    Returns:
        A cleaned Series with trimmed whitespace and title-case text.
    """
    return series.str.strip().str.title()


def convert_currency_to_float(series: pd.Series) -> pd.Series:
    """Convert a currency-formatted string column to float.

    Handles values like "$115,567,316.00" by stripping the
    currency symbol and thousands separators then converting to numeric.
    Non-convertible values become <NA>.
    """
    cleaned = (
        series.astype(str)
        .replace({'': pd.NA, 'nan': pd.NA, 'NA': pd.NA})
        .str.replace(r"[$,]", "", regex=True)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def fill_missing_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Fill missing numeric values using the column median.

    Using the median (rather than the mean) reduces the influence of
    outliers, which are common in box-office and rating data.

    Args:
        df: DataFrame containing the columns to fill.
        columns: List of numeric column names to fill.

    Returns:
        DataFrame with missing numeric values imputed.
    """
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            continue
        # Ensure column is numeric for median calculation
        df[col] = pd.to_numeric(df[col], errors="coerce")
        missing_count = int(df[col].isna().sum())
        if missing_count:
            median_value = df[col].median()
            if pd.isna(median_value):
                # nothing numeric to impute
                print(f"Column '{col}' contains no numeric values; skipping imputation.")
                continue
            df[col] = df[col].fillna(median_value)
            print(
                f"Filled {missing_count} missing value(s) in '{col}' "
                f"with median ({median_value:.2f})."
            )
    return df


def fill_missing_categorical(
    df: pd.DataFrame, columns: list[str], fill_value: str = "Unknown"
) -> pd.DataFrame:
    """Fill missing categorical/text values with a placeholder label.

    Args:
        df: DataFrame containing the columns to fill.
        columns: List of categorical column names to fill.
        fill_value: The placeholder string used to fill missing entries.

    Returns:
        DataFrame with missing categorical values filled.
    """
    df = df.copy()
    for col in columns:
        missing_count = df[col].isna().sum()
        if missing_count:
            df[col] = df[col].fillna(fill_value)
            print(f"Filled {missing_count} missing value(s) in '{col}' with '{fill_value}'.")
    return df


def enforce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to their correct, final data types.

    Args:
        df: DataFrame with cleaned but not-yet-typed columns.

    Returns:
        DataFrame with explicit, correct dtypes for every column.
    """
    df = df.copy()
    # Convert year to nullable integer (preserves missing values)
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    # Numeric columns
    for col in ["audience_score_pct", "rotten_tomatoes_pct", "profitability", "worldwide_gross"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Text columns: use pandas string dtype to preserve NA
    for col in ["genre", "lead_studio", "film"]:
        if col in df.columns:
            df[col] = df[col].astype("string").fillna(pd.NA)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full cleaning pipeline on the raw movies dataset.

    Pipeline steps:
        1. Rename columns to snake_case
        2. Standardize text formatting (genre, studio)
        3. Convert 'worldwide_gross' from currency string to float
        4. Fill missing numeric values with the column median
        5. Fill missing categorical values with 'Unknown'
        6. Remove duplicate rows
        7. Enforce final, correct data types

    Args:
        df: Raw movies DataFrame, as loaded from data/movies.csv.

    Returns:
        A cleaned, analysis-ready DataFrame.
    """
    df = rename_columns(df)

    df["genre"] = clean_text_column(df["genre"])
    df["lead_studio"] = df["lead_studio"].where(
        df["lead_studio"].isna(), df["lead_studio"].str.strip()
    )

    df["worldwide_gross"] = convert_currency_to_float(df["worldwide_gross"])

    df = fill_missing_numeric(df, ["audience_score_pct", "rotten_tomatoes_pct"])
    df = fill_missing_categorical(df, ["lead_studio"])

    df = remove_duplicate_rows(df)
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
