# 🎬 Movie Ratings Analysis Dashboard

An end-to-end Data Analytics portfolio project exploring movie performance
across audience scores, critic ratings (Rotten Tomatoes), studio, genre,
profitability, and box office gross — built with Python, Pandas, and an
interactive Streamlit dashboard.

> 🚧 **Project status:** In progress — being built and documented day by day.

---

## 📌 Project Overview

This project simulates a real-world data analyst workflow:

1. Load and explore a raw, messy dataset
2. Clean and preprocess it into an analysis-ready format
3. Perform exploratory data analysis (EDA) with visualizations
4. Build an interactive Streamlit dashboard for stakeholders
5. Polish the repository into a professional, interview-ready portfolio piece

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Pandas / NumPy | Data manipulation & analysis |
| Matplotlib / Seaborn | Static exploratory visualizations |
| Plotly | Interactive charts |
| Streamlit | Interactive dashboard |
| Git | Version control |
| Markdown | Documentation |

## 📁 Project Structure

```
movie-ratings-analysis/
│
├── data/                 # Raw and cleaned datasets
│   └── movies.csv
│
├── dashboard/             # Streamlit dashboard app
│   └── app.py
│
├── images/                # Saved charts from EDA
│
├── notebooks/              # Jupyter notebooks for exploration
│   └── analysis.ipynb
│
├── src/                   # Reusable, modular source code
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── visualization.py
│   └── analysis.py
│
├── outputs/                # Generated analysis outputs
│
├── requirements.txt
├── README.md
├── .gitignore
└── main.py
```

## 📊 Dataset

The dataset (`data/movies.csv`) contains one row per film with the
following fields:

| Column | Description |
|---|---|
| `Film` | Movie title |
| `Genre` | Primary genre |
| `Lead Studio` | Studio that led production |
| `Audience Score %` | Audience rating (0-100) |
| `Profitability` | Gross-to-budget ratio |
| `Rotten Tomatoes %` | Critic score on Rotten Tomatoes (0-100) |
| `Worldwide Gross` | Total worldwide box office revenue |
| `Year` | Release year |

> Note: The raw dataset intentionally includes real-world data quality
> issues (missing values, duplicate rows, inconsistent text casing, and
> currency-formatted strings) so the cleaning stage of this project
> reflects genuine data-wrangling work.




<!-- Day 2 section will be appended here -->

## 📄 License

This project is released under the MIT License (see `LICENSE`).
