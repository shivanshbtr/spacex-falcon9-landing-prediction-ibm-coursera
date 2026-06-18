# 🚀 SpaceX Falcon 9 First Stage Landing Prediction

> **IBM Applied Data Science Capstone — Coursera**

---

## 📌 Project Overview

SpaceX disrupted the rocket launch industry by making booster reuse economically viable. A Falcon 9 launch costs ~$62 million compared to $165+ million from competitors — largely because the first stage can be recovered and reflown. **Can we predict whether a first-stage booster will successfully land?**

This project collects real SpaceX launch data, analyses it through SQL and visualizations, maps launch sites interactively, and trains machine learning classifiers to answer exactly that question.

A full written report and slide deck are included in `Report_and_presentation/`.

---

## ⚠️ Note on Data Sources

The SpaceX public REST API (`api.spacexdata.com`) is **no longer available**. All notebooks use the **IBM Skills Network mirror datasets** hosted on AWS S3 — the same data the course was originally built around, stable and always accessible.

| Dataset              | IBM S3 path                                                   |
| -------------------- | ------------------------------------------------------------- |
| Part 1 (raw)         | `IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv`    |
| Part 2 (EDA)         | `IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv`    |
| Part 3 (ML features) | `IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv`    |
| SQL dataset          | `IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv`  |
| Geo dataset          | `IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv` |
| Dashboard CSV        | included at `app/spacex_launch_dash.csv`                    |

---

## 🗂️ Repository Structure

```
spacex-landing-prediction/
│
├── notebooks/
│   ├── 01_data_collection_api.ipynb          # Load, audit & clean IBM Part-1 dataset
│   ├── 02_data_collection_webscraping.ipynb  # Scrape Falcon 9 records from Wikipedia
│   ├── 03_data_wrangling.ipynb               # Clean, label & prepare the dataset
│   ├── 04_eda_visualization.ipynb            # EDA with Matplotlib & Seaborn
│   ├── 05_eda_sql.ipynb                      # EDA using SQL / SQLite
│   ├── 06_launch_site_map.ipynb              # Interactive maps with Folium
│   └── 07_predictive_models.ipynb            # ML models (LR, SVM, DT, KNN)
│
├── app/
│   ├── dashboard.py                          # Plotly Dash interactive dashboard
│   └── spacex_launch_dash.csv               # Dashboard data (included)
│
├── data/                                     # Saved outputs from notebook runs
│   ├── spacex_launches_raw.csv              # From notebook 01
│   ├── spacex_launches_wiki.csv             # From notebook 02 (Wikipedia scrape)
│   ├── spacex_wrangled.csv                  # From notebook 03 (90 rows × 18 cols)
│   ├── spacex_features.csv                  # ML feature matrix (one-hot encoded)
│   ├── spacex_labels.csv                    # Binary landing outcome (Class 0/1)
│   ├── spacex_launch_geo.csv               # Launch site coordinates
│   └── spacex.db                            # SQLite database for notebook 05
│
├── Report_and_presentation/
│   ├── Data Science Capstone Project Report.pdf
│   └── SpaceX_Capstone_Completed.pptx
│
└── README.md
```

---

## 🧪 Methods & Tools

| Phase               | Tools                                          |
| ------------------- | ---------------------------------------------- |
| Data Loading        | `requests`, IBM S3 hosted CSVs               |
| Web Scraping        | `BeautifulSoup`, Wikipedia                   |
| Data Wrangling      | `pandas`, `numpy`                          |
| EDA & Visualization | `matplotlib`, `seaborn`                    |
| SQL Analysis        | `SQLite`, `ipython-sql`                    |
| Interactive Maps    | `folium`                                     |
| Dashboard           | `plotly`, `dash`                           |
| Machine Learning    | `scikit-learn` (LR, SVM, Decision Tree, KNN) |

---

## 🔍 Key Questions Explored

1. Which launch sites have the highest success rates?
2. Does payload mass influence landing success?
3. How has the success rate changed over time (flight number)?
4. Which orbit types tend to see successful landings?
5. Which ML model best predicts first-stage landing success?

---

## 🏁 Results Summary

All four models were tuned with `GridSearchCV` and evaluated on an 80/20 train-test split of the wrangled dataset (90 rows × 18 features after one-hot encoding).

| Model                | Best Params                                         | CV Accuracy      | Test Accuracy |
| -------------------- | --------------------------------------------------- | ---------------- | ------------- |
| Logistic Regression  | `C=0.01, solver=lbfgs, max_iter=300`              | 86.25%           | 77.78%        |
| SVM                  | `C=0.01, kernel=linear, gamma=scale`              | 85.00%           | 77.78%        |
| Decision Tree        | `criterion=gini, max_depth=2, min_samples_leaf=1` | 85.00%           | 77.78%        |
| K-Nearest Neighbours | `n_neighbors=9, p=1, weights=uniform`             | **87.86%** | 77.78%        |

All four models converge to the same test accuracy (77.78%), which reflects the small dataset size (~90 rows after wrangling) rather than a model limitation. KNN edges ahead on cross-validation score.

**Key predictors:** flight number (experience), payload mass, orbit type, and launch site.
**Notable finding:** Success rate improved significantly from 2013 onward as SpaceX refined its landing technology.

---

## ⚙️ Setup & Running

### 1. Clone the repo

```bash
git clone https://github.com/shivanshbtr/spacex-landing-prediction.git
cd spacex-landing-prediction
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn folium plotly dash requests beautifulsoup4 sqlalchemy ipython-sql wget
```

### 3. Run notebooks in order

Open Jupyter and run notebooks `01` → `07` in sequence. Intermediate outputs are saved to `data/` so individual notebooks can be re-run independently.

### 4. Launch the dashboard

The dashboard CSV is already included in `app/`. Simply run:

```bash
cd app
python dashboard.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

---

## 📊 Dashboard Features

- **Site Selector Dropdown** — filter by launch site or view all sites combined
- **Pie Chart** — success/failure distribution for the selected site (donut style)
- **Payload Range Slider** — filter the scatter plot by payload mass (0–10,000 kg, step 500)
- **Scatter Plot** — payload mass vs. landing outcome, coloured by booster version category

---

## 🙏 Acknowledgements

- IBM Skills Network / Coursera Applied Data Science Capstone
- [Wikipedia — List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)
