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

import pandas as pd
import plotly.express as px
import streamlit as st

# Allow importing from src/ when Streamlit runs this file directly
sys.path.append(str(Path(__file__).resolve().parent.parent))

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
    col3.metric("Highest Grossing", top_film["film"], f"${top_film['worldwide_gross']:,.0f}")
    col4.metric("Avg Rotten Tomatoes", f"{df['rotten_tomatoes_pct'].mean():.1f}%")


def render_charts(df: pd.DataFrame) -> None:
    """Render the four interactive Plotly charts in a 2x2 grid."""
    if df.empty:
        st.warning("No movies match the selected filters. Try widening your selection.")
        return

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Genre Share")
        genre_counts = df["genre"].value_counts().reset_index()
        genre_counts.columns = ["genre", "count"]
        fig_pie = px.pie(
            genre_counts, names="genre", values="count", hole=0.4,
            color_discrete_sequence=px.colors.sequential.Viridis,
        )
        st.plotly_chart(fig_pie, width="stretch")

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
        st.subheader("Profitability vs. Audience Score")
        fig_scatter = px.scatter(
            df, x="audience_score_pct", y="profitability", color="genre",
            hover_data=["film", "lead_studio", "year"],
            labels={"audience_score_pct": "Audience Score %", "profitability": "Profitability"},
        )
        st.plotly_chart(fig_scatter, width="stretch")


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


if __name__ == "__main__":
    main()