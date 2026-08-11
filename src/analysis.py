"""analysis.py - Aggregation and statistical analysis functions."""

import pandas as pd


def genre_counts(df: pd.DataFrame) -> pd.Series:
    """Count the number of films per genre, sorted descending."""
    return df["genre"].value_counts()


def average_gross_by_genre(df: pd.DataFrame) -> pd.Series:
    """Compute average worldwide gross per genre, sorted descending."""
    return df.groupby("genre")["worldwide_gross"].mean().sort_values(ascending=False)


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the Pearson correlation matrix for numeric columns."""
    numeric_cols = ["audience_score_pct", "rotten_tomatoes_pct", "profitability", "worldwide_gross", "year"]
    return df[numeric_cols].corr()


def releases_per_year(df: pd.DataFrame) -> pd.Series:
    """Count the number of films released per year."""
    return df.groupby("year").size().sort_index()


def top_grossing_film(df: pd.DataFrame) -> pd.Series:
    """Return the row for the highest-grossing film in the dataset."""
    return df.loc[df["worldwide_gross"].idxmax()]


def summary_kpis(df: pd.DataFrame) -> dict:
    """Compute headline KPIs used in the README and dashboard."""
    top_film = top_grossing_film(df)
    return {
        "total_movies": len(df),  # len() already returns a plain int
        "avg_audience_score": round(df["audience_score_pct"].mean(), 1),
        "avg_rotten_tomatoes": round(df["rotten_tomatoes_pct"].mean(), 1),
        "avg_profitability": round(df["profitability"].mean(), 2),
        "highest_grossing_film": top_film["film"],
        # float()/int() below convert numpy scalars (np.float64/np.int64)
        # to native Python types for clean printing/JSON serialization.
        "highest_grossing_amount": float(top_film["worldwide_gross"]),
        "most_common_genre": df["genre"].value_counts().idxmax(),
        "year_range": (int(df["year"].min()), int(df["year"].max())),
    }