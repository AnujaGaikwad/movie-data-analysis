"""
Interactive Streamlit dashboard for the Movie Ratings Analysis project.

Run with:
    streamlit run dashboard/app.py

Features:
    - KPI cards (total movies, avg audience score, highest grossing film,
      avg Rotten Tomatoes score)
    - Sidebar filters (genre, year range)
    - Interactive Plotly charts (pie, bar, histogram, scatter) that all
      respond live to the sidebar filters
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Allow importing from src/ when Streamlit runs this file directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.analysis import average_profitability_by_studio, generate_key_insights
from src.cleaning import clean_data
from src.data_loader import load_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "movies_cleaned.csv"
RAW_DATA_PATH = PROJECT_ROOT / "data" / "movies.csv"


@st.cache_data
def get_data() -> pd.DataFrame:
    """Load the cleaned movies dataset, cleaning it on the fly if needed.

    Prefers the pre-cleaned CSV saved by the Day 2 pipeline. Falls back
    to cleaning the raw dataset live so the dashboard works even if
    main.py hasn't been run yet.
    """
    if CLEANED_DATA_PATH.exists():
        return pd.read_csv(CLEANED_DATA_PATH)
    return clean_data(load_data(RAW_DATA_PATH))


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filter widgets and return the filtered DataFrame."""
    st.sidebar.header("🔍 Filters")

    genres = sorted(df["genre"].unique())
    selected_genres = st.sidebar.multiselect(
        "Genre", options=genres, default=genres
    )

    year_min, year_max = int(df["year"].min()), int(df["year"].max())
    selected_years = st.sidebar.slider(
        "Year", min_value=year_min, max_value=year_max, value=(year_min, year_max)
    )

    filtered = df[
        df["genre"].isin(selected_genres)
        & df["year"].between(selected_years[0], selected_years[1])
    ]

    st.sidebar.markdown(f"**{len(filtered)}** of **{len(df)}** movies match your filters.")
    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    """Render the top-row KPI metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    if df.empty:
        for col, label in zip([col1, col2, col3, col4], ["Total Movies", "Avg Audience Score", "Highest Grossing", "Avg Rotten Tomatoes"]):
            col.metric(label, "N/A")
        return

    top_film = df.loc[df["worldwide_gross"].idxmax()]

    col1.metric("Total Movies", f"{len(df):,}")
    col2.metric("Avg Audience Score", f"{df['audience_score_pct'].mean():.1f}%")
    # Fix #3: no `delta=` here. A delta renders as a green/red arrow, which
    # implies a comparison against something (last period, a target, etc.)
    # that doesn't exist. The gross is shown as a plain caption instead.
    col3.metric("Highest Grossing Movie", top_film["film"])
    col3.caption(f"Worldwide Gross: ${top_film['worldwide_gross']:,.0f}")
    col4.metric("Avg Rotten Tomatoes", f"{df['rotten_tomatoes_pct'].mean():.1f}%")


def render_charts(df: pd.DataFrame) -> None:
    """Render the interactive Plotly charts in a grid."""
    if df.empty:
        st.warning("No movies match the selected filters. Try widening your selection.")
        return

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # Fix #5: donut -> horizontal bar. Harder to compare 10 similarly
        # sized wedges by eye than 10 bars of different length.
        st.subheader("Genre Distribution")
        genre_counts = df["genre"].value_counts().sort_values().reset_index()
        genre_counts.columns = ["genre", "count"]
        fig_bar_genre = px.bar(
            genre_counts, x="count", y="genre", orientation="h",
            labels={"count": "Number of Films", "genre": "Genre"},
            color="count", color_continuous_scale="Viridis",
        )
        fig_bar_genre.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar_genre, width="stretch")

    with row1_col2:
        st.subheader("Average Worldwide Gross by Genre")
        avg_gross = (
            df.groupby("genre")["worldwide_gross"].mean().sort_values(ascending=False) / 1_000_000
        ).reset_index()
        avg_gross.columns = ["genre", "avg_gross_millions"]
        fig_bar = px.bar(
            avg_gross, x="genre", y="avg_gross_millions",
            labels={"avg_gross_millions": "Avg Worldwide Gross ($M)", "genre": "Genre"},
            color="avg_gross_millions", color_continuous_scale="Viridis",
        )
        fig_bar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar, width="stretch")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Audience Score Distribution")
        fig_hist = px.histogram(
            df, x="audience_score_pct", nbins=20,
            labels={"audience_score_pct": "Audience Score %"},
            color_discrete_sequence=["#3b528b"],
        )
        st.plotly_chart(fig_hist, width="stretch")

    with row2_col2:
        # Fix #2: single color instead of one-per-genre (reduces visual
        # noise) + a manually fitted trendline + the printed correlation
        # coefficient, so the chart states its own conclusion instead of
        # leaving the viewer to eyeball a cloud of dots.
        st.subheader("Profitability vs. Audience Score")
        corr_value = df["audience_score_pct"].corr(df["profitability"])
        if abs(corr_value) < 0.005:
            corr_value = 0.0
        st.caption(f"Correlation: {corr_value:.2f} (\u22481.0 = strong positive, \u22480 = none, \u2248-1.0 = strong negative)")

        fig_scatter = px.scatter(
            df, x="audience_score_pct", y="profitability",
            hover_data=["film", "genre", "lead_studio", "year"],
            labels={"audience_score_pct": "Audience Score %", "profitability": "Profitability"},
            color_discrete_sequence=["#3b528b"],
            opacity=0.65,
        )
        if len(df) >= 2 and df["audience_score_pct"].nunique() >= 2:
            slope, intercept = np.polyfit(df["audience_score_pct"], df["profitability"], 1)
            x_line = np.array([df["audience_score_pct"].min(), df["audience_score_pct"].max()])
            fig_scatter.add_trace(
                go.Scatter(
                    x=x_line, y=slope * x_line + intercept,
                    mode="lines", name="Trend", line=dict(color="#E63950", width=2.5),
                )
            )
        st.plotly_chart(fig_scatter, width="stretch")

    # Fix #7 (studio question): a genuinely new analytical angle using the
    # lead_studio column, which the original dashboard collected but never
    # used.
    st.subheader("Average Profitability by Studio")
    st.caption("Studios with at least 3 films in the current filtered dataset")
    studio_profit = average_profitability_by_studio(df, min_films=3)
    if studio_profit.empty:
        st.info("Not enough films per studio in the current filter selection to compare studios.")
    else:
        studio_df = studio_profit.reset_index()
        studio_df.columns = ["lead_studio", "avg_profitability"]
        fig_studio = px.bar(
            studio_df, x="avg_profitability", y="lead_studio", orientation="h",
            labels={"avg_profitability": "Avg Profitability (x budget)", "lead_studio": "Studio"},
            color="avg_profitability", color_continuous_scale="Viridis",
        )
        fig_studio.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig_studio, width="stretch")


def render_key_insights(df: pd.DataFrame) -> None:
    """Fix #4/#6: a plain-language insights section computed live from the
    currently filtered data (via analysis.generate_key_insights), plus a
    business takeaway that is explicitly framed as correlation, not
    causation, and scoped to what this dataset can actually support."""
    st.subheader("\U0001F4CC Key Insights")
    for line in generate_key_insights(df):
        st.markdown(f"- {line}")

    st.subheader("Business Takeaway")
    st.markdown(
        "- High audience or critic ratings alone are not a reliable predictor "
        "of profitability in this dataset \u2014 genre and studio track record "
        "show a stronger relationship with financial performance than ratings do.\n"
        "- These are correlations, not causes: factors this dataset doesn't "
        "capture \u2014 marketing spend, franchise recognition, release "
        "timing, screen count \u2014 likely explain more of the variation."
    )


def main() -> None:
    """Configure the page and render the full dashboard."""
    st.set_page_config(page_title="Movie Ratings Analysis Dashboard", page_icon="🎬", layout="wide")

    st.title("🎬 Movie Ratings Analysis Dashboard")
    st.markdown(
        "Explore audience scores, critic ratings, profitability, and box "
        "office performance across genres and years."
    )

    df = get_data()
    filtered_df = render_sidebar_filters(df)

    render_kpis(filtered_df)
    st.divider()
    render_charts(filtered_df)
    st.divider()
    render_key_insights(filtered_df)


if __name__ == "__main__":
    main()
