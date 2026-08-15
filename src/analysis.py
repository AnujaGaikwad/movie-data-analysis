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


def average_profitability_by_studio(df: pd.DataFrame, min_films: int = 3) -> pd.Series:
    """Average profitability per studio, restricted to studios with at
    least `min_films` entries so a single outlier movie can't make a
    studio look artificially strong or weak. Excludes "Unknown" - that's
    a placeholder cleaning.py fills in for missing studio data, not a
    real studio, and would be misleading in a ranking."""
    known = df[df["lead_studio"] != "Unknown"]
    counts = known["lead_studio"].value_counts()
    eligible = counts[counts >= min_films].index
    subset = known[known["lead_studio"].isin(eligible)]
    return (
        subset.groupby("lead_studio")["profitability"]
        .mean()
        .sort_values(ascending=False)
    )


def _describe_correlation(value: float) -> str:
    """Turn a Pearson correlation coefficient into a plain-language strength
    label, so auto-generated insight text stays accurate as filters change
    the underlying subset (rather than assuming it's always weak, which
    was true for the full dataset but isn't guaranteed for every filter)."""
    magnitude = abs(value)
    if magnitude < 0.1:
        return "essentially no relationship"
    elif magnitude < 0.3:
        strength = "a weak"
    elif magnitude < 0.5:
        strength = "a moderate"
    else:
        strength = "a strong"
    direction = "positive" if value > 0 else "negative"
    return f"{strength} {direction} relationship"


def generate_key_insights(df: pd.DataFrame) -> list[str]:
    """Compute a short list of plain-language insights directly from the
    current DataFrame. Every number here is calculated live, not written
    by hand, so it stays accurate if the data changes."""
    insights = []
    if df.empty or len(df) < 5:
        return ["Not enough movies match the current filters to compute insights."]

    corr = correlation_matrix(df)
    audience_profit_corr = corr.loc["audience_score_pct", "profitability"]
    rt_profit_corr = corr.loc["rotten_tomatoes_pct", "profitability"]
    # Guard against the "-0.00" display artifact when a value rounds to
    # zero but keeps a negative sign.
    if abs(audience_profit_corr) < 0.005:
        audience_profit_corr = 0.0
    if abs(rt_profit_corr) < 0.005:
        rt_profit_corr = 0.0

    insights.append(
        f"Audience score has {_describe_correlation(audience_profit_corr)} with "
        f"profitability ({audience_profit_corr:.2f}); critic score has "
        f"{_describe_correlation(rt_profit_corr)} with profitability "
        f"({rt_profit_corr:.2f})."
    )

    gross_by_genre = average_gross_by_genre(df)
    if len(gross_by_genre) >= 2:
        top_genre, bottom_genre = gross_by_genre.index[0], gross_by_genre.index[-1]
        insights.append(
            f"{top_genre} leads in average worldwide gross "
            f"(${gross_by_genre.iloc[0]/1e6:,.1f}M), while {bottom_genre} trails "
            f"(${gross_by_genre.iloc[-1]/1e6:,.1f}M)."
        )

    aud_mean = df["audience_score_pct"].mean()
    rt_mean = df["rotten_tomatoes_pct"].mean()
    gap = aud_mean - rt_mean
    direction = "higher than" if gap > 0 else "lower than" if gap < 0 else "about the same as"
    insights.append(
        f"Average audience score ({aud_mean:.1f}%) is {direction} average critic "
        f"score ({rt_mean:.1f}%), a gap of {abs(gap):.1f} points."
    )

    studio_profit = average_profitability_by_studio(df)
    if len(studio_profit) >= 2:
        insights.append(
            f"Among studios with several releases in this dataset, "
            f"{studio_profit.index[0]} has the highest average profitability "
            f"({studio_profit.iloc[0]:.2f}x)."
        )

    return insights
