"""
Visualization utilities for the movie-ratings project.

Each function creates a specific Matplotlib figure, saves it as a PNG
to the supplied path, and returns the Figure object.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Consistent styling for all figures
sns.set_theme(style="whitegrid", palette="viridis")


def _save(fig: plt.Figure, save_path: str) -> None:
    """Save a Matplotlib figure to disk with automatic directory creation."""
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    # Save with good resolution and minimal extra whitespace
    fig.savefig(save_path, dpi=150, bbox_inches="tight")


def plot_genre_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Create a horizontal bar chart showing the number of films per genre."""
    # Count films in each genre and sort from lowest to highest
    counts = df["genre"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.barh(
        counts.index,
        counts.values,
        color=sns.color_palette("viridis", len(counts))
    )

    ax.set_title("Number of Films by Genre", fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Films")
    ax.set_ylabel("Genre")

    _save(fig, save_path)
    return fig


def plot_audience_score_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Create a histogram showing the distribution of audience scores."""
    fig, ax = plt.subplots(figsize=(9, 6))

    sns.histplot(
        df["audience_score_pct"],
        bins=20,
        kde=True,
        ax=ax,
        color="#3b528b"
    )

    ax.set_title("Distribution of Audience Score (%)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Audience Score %")
    ax.set_ylabel("Number of Films")

    _save(fig, save_path)
    return fig


def plot_rotten_tomatoes_distribution(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the distribution of Rotten Tomatoes scores as a histogram."""
    fig, ax = plt.subplots(figsize=(9, 6))

    sns.histplot(
        df["rotten_tomatoes_pct"],
        bins=20,
        kde=True,
        ax=ax,
        color="#21918c"
    )

    ax.set_title(
        "Distribution of Rotten Tomatoes Score (%)",
        fontsize=14,
        fontweight="bold"
    )
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

    ax.bar(
        avg_gross.index,
        avg_gross.values,
        color=sns.color_palette("viridis", len(avg_gross))
    )

    ax.set_title("Average Worldwide Gross by Genre", fontsize=14, fontweight="bold")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Average Worldwide Gross ($ Millions)")

    plt.xticks(rotation=45, ha="right")

    _save(fig, save_path)
    return fig


def plot_profitability_vs_audience(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot profitability against audience score as a scatter plot."""
    fig, ax = plt.subplots(figsize=(9, 6))

    sns.scatterplot(
        data=df,
        x="audience_score_pct",
        y="profitability",
        hue="genre",
        ax=ax,
        alpha=0.75,
        s=60
    )

    ax.set_title("Profitability vs. Audience Score", fontsize=14, fontweight="bold")
    ax.set_xlabel("Audience Score %")
    ax.set_ylabel("Profitability (Gross-to-Budget Ratio)")
    ax.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        fontsize=8,
        title="Genre"
    )

    _save(fig, save_path)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot a correlation heatmap of the numeric columns."""
    numeric_cols = [
        "audience_score_pct",
        "rotten_tomatoes_pct",
        "profitability",
        "worldwide_gross",
        "year"
    ]

    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="viridis",
        ax=ax,
        square=True,
        cbar_kws={"shrink": 0.8}
    )

    ax.set_title(
        "Correlation Heatmap of Numeric Features",
        fontsize=14,
        fontweight="bold"
    )

    _save(fig, save_path)
    return fig


def plot_yearwise_releases(df: pd.DataFrame, save_path: str) -> plt.Figure:
    """Plot the number of films released per year as a line chart."""
    counts = df.groupby("year").size().sort_index()

    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(
        counts.index,
        counts.values,
        marker="o",
        color="#440154",
        linewidth=2
    )

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