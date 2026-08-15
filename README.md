# 🎬 Movie Ratings Analysis

<p align="center">
  <strong>An end-to-end Data Analytics project exploring movie ratings, profitability, studio performance, genre trends, and worldwide box office revenue.</strong>
</p>

<p align="center">
  Built with Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, and Streamlit.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458" alt="Pandas">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B" alt="Streamlit">
  <img src="https://img.shields.io/badge/Status-Complete-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

---

## 📌 Project Overview

This project demonstrates a complete **Data Analytics workflow**, starting with a raw movie dataset and ending with an interactive dashboard.

### Workflow

**Raw Data → Data Cleaning → EDA → Analysis → Visualization → Interactive Dashboard → Business Insights**

The analysis explores how **audience ratings, critic ratings, profitability, genre, studio, release year, and worldwide gross** relate to movie performance.

---

## ✨ Key Features

* 🧹 **Data Cleaning & Preprocessing**

  * Missing-value analysis
  * Duplicate detection
  * Data-type correction
  * Currency and numeric-value cleaning
  * Reproducible cleaning pipeline

* 📊 **Exploratory Data Analysis**

  * Genre distribution
  * Audience score distribution
  * Critic score distribution
  * Worldwide gross by genre
  * Profitability vs. audience score
  * Correlation analysis
  * Year-wise release trends

* 🖥️ **Interactive Streamlit Dashboard**

  * Dynamic KPI cards
  * Genre filtering
  * Year filtering
  * Interactive Plotly charts
  * Filter-dependent insights

* 📈 **Business-Focused Analysis**

  * Average profitability by studio
  * Correlation between ratings and profitability
  * Genre performance comparison
  * Worldwide gross analysis
  * Plain-language business takeaways

* 📓 **Jupyter Notebook**

  * Step-by-step exploration
  * Data cleaning
  * EDA
  * Analysis and interpretation

---

## 🧰 Tech Stack

| Category        | Tools                       |
| --------------- | --------------------------- |
| Programming     | Python                      |
| Data Analysis   | Pandas, NumPy               |
| Visualization   | Matplotlib, Seaborn, Plotly |
| Dashboard       | Streamlit                   |
| Development     | Jupyter Notebook, VS Code   |
| Version Control | Git, GitHub                 |
| Documentation   | Markdown                    |

---

## 📊 Dataset

The dataset contains one row per film with information about ratings, profitability, studio, genre, release year, and worldwide revenue.

| Column              | Description                      |
| ------------------- | -------------------------------- |
| `Film`              | Movie title                      |
| `Genre`             | Primary movie genre              |
| `Lead Studio`       | Studio associated with the movie |
| `Audience Score %`  | Audience rating from 0–100       |
| `Profitability`     | Gross-to-budget ratio            |
| `Rotten Tomatoes %` | Critic score from 0–100          |
| `Worldwide Gross`   | Worldwide box office revenue     |
| `Year`              | Movie release year               |

---

## 🔍 Key Insights

The analysis produced several notable findings:

* **Profitability has almost no correlation with audience score or critic score** in this dataset (`r ≈ 0.00`).
* A highly rated movie is therefore **not necessarily a highly profitable movie**.
* **Action, Romance, and Horror** show the highest average worldwide gross among the analyzed genres.
* **Documentary and Fantasy** have comparatively lower average worldwide gross.
* Audience and critic scores follow broadly similar distributions, although critic scores show slightly greater variation.
* Movie release volume fluctuates across the analyzed years without a strong long-term trend.

> **Important:** Correlation does not imply causation.
> The analysis identifies relationships in the dataset, not proof that ratings directly cause profitability or revenue.

---

## 📈 Dashboard

The Streamlit dashboard provides an interactive way to explore the dataset.

### Dashboard includes

* **KPI Cards**

  * Total movies
  * Average audience score
  * Average critic score
  * Average profitability
  * Total worldwide gross

* **Interactive Charts**

  * Genre distribution
  * Worldwide gross by genre
  * Score distributions
  * Profitability vs. audience score
  * Correlation analysis

* **Filters**

  * Genre
  * Release year

The insights update according to the selected filters.

---

## 🖼️ Dashboard Preview

| Dashboard                                  | Analysis                         |
| ------------------------------------------ | -------------------------------- |
| `images/screenshot_dashboard_overview.png` | Dashboard overview               |
| `images/screenshot_dashboard_filters.png`  | Genre and year filters           |
| `images/screenshot_kpi_cards.png`          | KPI cards                        |
| `images/screenshot_genre_pie_chart.png`    | Genre distribution               |
| `images/screenshot_scatter_chart.png`      | Profitability vs. audience score |

---

## 📁 Project Structure

```text
movie-ratings-analysis/
│
├── data/
│   ├── movies.csv
│   └── movies_cleaned.csv
│
├── dashboard/
│   └── app.py
│
├── images/
│   ├── EDA charts
│   └── dashboard screenshots
│
├── notebooks/
│   └── analysis.ipynb
│
├── src/
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── visualization.py
│   └── analysis.py
│
├── outputs/
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── main.py
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/movie-ratings-analysis.git
cd movie-ratings-analysis
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Run the data pipeline

```bash
python main.py
```

This performs the project workflow:

```text
Load → Clean → Analyze → Generate Visualizations
```

### Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

### Explore the notebook

```bash
jupyter notebook notebooks/analysis.ipynb
```

## 🎯 What This Project Demonstrates

This project demonstrates practical skills in:

* Data loading and inspection
* Data cleaning and preprocessing
* Exploratory Data Analysis
* Statistical correlation analysis
* Data visualization
* Aggregation and grouping
* Business-oriented interpretation
* Interactive dashboard development
* Modular Python development
* Git and GitHub workflow
* Project documentation

---

## 📄 Requirements

Project dependencies are listed in:

```text
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 📜 License

This project is licensed under the **MIT License**.

---

<p align="center">
  🎬 <strong>Movie Ratings Analysis Dashboard</strong>
  <br>
  Built with Python • Pandas • Visualization • Streamlit
</p>
