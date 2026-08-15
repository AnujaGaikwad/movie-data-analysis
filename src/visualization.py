"""
visualization.py
-----------------
Chart-generation functions for exploratory data analysis.

Every function saves a chart as a PNG to the given output path and
also returns the Matplotlib Figure, so charts can be displayed inline
in a notebook AND saved to disk from a script in one call.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")


def _save(fig: plt.Figure, save_path: str) -> None:
    """Save a figure to disk, creating parent directories if needed."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(save_path, dpi=150, bbox_inches="tight")


def plot_genre_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the number of films per genre as a horizontal bar chart."""
    counts = df["genre"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(counts.index, counts.values, color=sns.color_palette("viridis", len(counts)))
    ax.set_title("Number of Films by Genre", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Films")
    ax.set_ylabel("Genre")
    _save(fig, save_path)
    return fig


def plot_audience_score_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the distribution of audience scores as a histogram."""
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.histplot(df["audience_score_pct"], bins=20, kde=True, ax=ax, color="#3b528b")
    ax.set_title("Distribution of Audience Score (%)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Audience Score %")
    ax.set_ylabel("Number of Films")
    _save(fig, save_path)
    return fig


def plot_rotten_tomatoes_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the distribution of Rotten Tomatoes scores as a histogram."""
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.histplot(df["rotten_tomatoes_pct"], bins=20, kde=True, ax=ax, color="#21918c")
    ax.set_title("Distribution of Rotten Tomatoes Score (%)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Rotten Tomatoes %")
    ax.set_ylabel("Number of Films")
    _save(fig, save_path)
    return fig


def plot_gross_by_genre(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot average worldwide gross per genre as a bar chart."""
    avg_gross = (
        df.groupby("genre")["worldwide_gross"].mean().sort_values(ascending=False) / 1_000_000
    )
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.bar(avg_gross.index, avg_gross.values, color=sns.color_palette("viridis", len(avg_gross)))
    ax.set_title("Average Worldwide Gross by Genre", fontsize=14, fontweight="bold")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Worldwide Gross ($ Millions)")
    plt.xticks(rotation=45, ha="right")
    _save(fig, save_path)
    return fig


def plot_profitability_vs_audience(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot profitability against audience score as a scatter plot, with a
    fitted trendline and the printed correlation coefficient. Uses a single
    color rather than one-per-genre: with 10 genres, a color legend adds
    visual noise without making the actual relationship (or lack of one)
    any easier to read - the trendline and coefficient communicate that
    directly instead."""
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        data=df, x="audience_score_pct", y="profitability",
        ax=ax, alpha=0.65, s=55, color="#3b528b",
    )

    corr_value = df["audience_score_pct"].corr(df["profitability"])
    if abs(corr_value) < 0.005:
        corr_value = 0.0
    if df["audience_score_pct"].nunique() >= 2:
        slope, intercept = np.polyfit(df["audience_score_pct"], df["profitability"], 1)
        x_line = np.array([df["audience_score_pct"].min(), df["audience_score_pct"].max()])
        ax.plot(x_line, slope * x_line + intercept, color="#E63950", linewidth=2.2, label="Trend")
        ax.legend(loc="upper left", fontsize=9)

    ax.set_title(
        f"Profitability vs. Audience Score  (r = {corr_value:.2f})",
        fontsize=14, fontweight="bold",
    )
    ax.set_xlabel("Audience Score %")
    ax.set_ylabel("Profitability (Gross-to-Budget Ratio)")
    _save(fig, save_path)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot a correlation heatmap of the numeric columns."""
    numeric_cols = ["audience_score_pct", "rotten_tomatoes_pct", "profitability", "worldwide_gross", "year"]
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="viridis", ax=ax, square=True, cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Heatmap of Numeric Features", fontsize=14, fontweight="bold")
    _save(fig, save_path)
    return fig


def plot_yearwise_releases(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the number of films released per year as a line chart."""
    counts = df.groupby("year").size().sort_index()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.plot(counts.index, counts.values, marker="o", color="#440154", linewidth=2)
    ax.set_title("Year-wise Movie Releases", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Films Released")
    _save(fig, save_path)
    return fig


def generate_all_charts(df: pd.DataFrame, output_dir: str) -> None:
    """Generate and save every EDA chart used in this project."""
    out = Path(output_dir)
    charts = {
        "genre_distribution.png": plot_genre_distribution,
        "audience_score_distribution.png": plot_audience_score_distribution,
        "rotten_tomatoes_distribution.png": plot_rotten_tomatoes_distribution,
        "gross_by_genre.png": plot_gross_by_genre,
        "profitability_vs_audience_score.png": plot_profitability_vs_audience,
        "correlation_heatmap.png": plot_correlation_heatmap,
        "yearwise_releases.png": plot_yearwise_releases,
    }
    for filename, plot_fn in charts.items():
        fig = plot_fn(df, str(out / filename))
        plt.close(fig)
        print(f"Saved chart: {out / filename}")
