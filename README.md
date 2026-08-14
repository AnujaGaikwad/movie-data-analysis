
<h1 align="center">🎬 Movie Ratings Analysis Dashboard</h1>

<p align="center">
  An end-to-end data analytics portfolio project exploring movie performance —
  audience scores, critic ratings, profitability, and box office gross —
  from raw CSV to an interactive Streamlit dashboard.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/status-complete-brightgreen" alt="Status: complete">
  <img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License: MIT">
</p>

---

## 📌 Overview

This project follows a complete, real-world data analyst workflow:

1. **Load & explore** a raw, messy movies dataset
2. **Clean & preprocess** it into an analysis-ready format
3. **Explore** the data visually (EDA) and surface real insights
4. **Build** an interactive Streamlit dashboard for stakeholders
5. **Document & polish** the repository into an interview-ready portfolio piece

## ✨ Features

- 🧹 **Reproducible cleaning pipeline** — missing values, duplicates, wrong
  dtypes, and currency strings handled with modular, tested functions
- 📊 **7 exploratory charts** — genre distribution, score distributions,
  gross by genre, profitability vs. audience score, correlation heatmap,
  and year-wise release trends, each saved as PNG and documented
- 🖥️ **Interactive dashboard** — live KPI cards, genre/year filters, and
  4 Plotly charts (pie, bar, histogram, scatter) that update instantly
- 📓 **Companion Jupyter notebook** mirroring the full analysis, cell by cell
- 🗂️ **Clean, modular codebase** — type hints, docstrings, PEP8-compliant,
  organized into single-responsibility modules under `src/`

## 🧰 Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data manipulation | Pandas, NumPy |
| Static visualization | Matplotlib, Seaborn |
| Interactive visualization | Plotly |
| Dashboard | Streamlit |
| Version control | Git / GitHub |
| Documentation | Markdown, Jupyter |

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/movie-ratings-analysis.git
cd movie-ratings-analysis

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

```bash
# Run the full data pipeline: load → clean → analyze → generate charts
python main.py

# Launch the interactive dashboard
streamlit run dashboard/app.py
```

Optionally, explore the analysis step-by-step in Jupyter:
```bash
jupyter notebook notebooks/analysis.ipynb
```

## 🖼️ Screenshots

> Screenshots below are placeholders — replace each with a real capture of
> your running dashboard (`streamlit run dashboard/app.py`, then screenshot
> your browser window) before publishing.

| Screenshot | File |
|---|---|
| Dashboard overview (KPIs + all charts) | `images/screenshot_dashboard_overview.png` |
| Sidebar filters in use (genre + year) | `images/screenshot_dashboard_filters.png` |
| KPI cards close-up | `images/screenshot_kpi_cards.png` |
| Genre share pie chart | `images/screenshot_genre_pie_chart.png` |
| Profitability vs. audience score scatter | `images/screenshot_scatter_chart.png` |

## 📁 Project Structure

```text
movie-ratings-analysis/
│
├── data/
│   ├── movies.csv               # Raw dataset
│   └── movies_cleaned.csv       # Cleaned, analysis-ready dataset
│
├── dashboard/
│   └── app.py                   # Streamlit dashboard
│
├── images/                      # Saved EDA charts + screenshots
│
├── notebooks/
│   └── analysis.ipynb           # Step-by-step exploration notebook
│
├── src/
│   ├── data_loader.py           # Load + inspect data
│   ├── cleaning.py              # Cleaning pipeline
│   ├── visualization.py         # Chart-generation functions
│   └── analysis.py              # KPIs, correlations, aggregations
│
├── outputs/                     # Reserved for exported reports/results
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── main.py                      # Pipeline entry point
```

## 📊 Dataset

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

## 🔍 Key Insights

- Profitability shows **almost no correlation** with audience score or
  critic score (r ≈ 0.00) — a well-loved film isn't necessarily a
  profitable one, and vice versa.
- **Action, Romance, and Horror** lead in average worldwide gross;
  Documentary and Fantasy trail.
- Audience scores and critic scores are both roughly bell-shaped, with
  critics slightly more spread out and marginally harsher on average.
- Release volume fluctuates year to year with no strong long-term trend
  across the 2007-2023 window covered by this dataset.

## 🗓️ Development Log

| Day | Focus | Status |
|---|---|---|
| 1 | Project setup & dataset exploration | ✅ |
| 2 | Data cleaning & preprocessing | ✅ |
| 3 | Exploratory data analysis (7 charts) | ✅ |
| 4 | Interactive Streamlit dashboard | ✅ |
| 5 | Final documentation & GitHub release | ✅ |

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes with a clear message
4. Push to your branch and open a Pull Request

Please keep new code consistent with the existing style: type hints,
docstrings, and PEP8 formatting (checked with `flake8`).

## 📄 Requirements

See [`requirements.txt`](requirements.txt) for the full dependency list.

## 📜 License

This project is released under the [MIT License](LICENSE).

---

<p align="center">Built as a data analytics  project.</p>
````

## One thing worth deciding
You dropped the **"🔮 Future Improvements"** section entirely — that's fine if intentional (it's optional), but it's a small, easy signal in interviews ("here's what I'd do next with more time"). Want me to add it back in, or are you keeping the README lean on purpose?
