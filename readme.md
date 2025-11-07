# 📊 Football Recruitment Decision Support Tool (MAVT)

## 📝 Overview
This project develops a **Multi-Criteria Decision Making (MCDM)** tool to support player recruitment decisions for professional football clubs.  
It is based on the real case of **Stade Brestois 29**, which qualified for the **2024/2025 UEFA Champions League**, and seeks to recruit a **high-level striker** while balancing sporting ambitions and financial constraints.

The method used is **MAVT (Multi-Attribute Value Theory)**, applied to evaluate striker profiles according to the priorities of two decision-makers:
- **Head Coach** → sporting performance and tactical fit  
- **Club President** → financial sustainability, reputation, and long-term development vision  

A compromise approach is used to identify players who meet both sets of expectations.

---

## 📂 Project Structure

```
football_recruitement_tool/
│   myrequirements.txt
│   readme.md
│   __init__.py
│
├── data/
│   ├── raw_data_players_2023.csv
│   ├── top_players.csv
│   └── __init__.py
│
├── football_recruitement_tool/
│   ├── config_value_functions.py
│   ├── config_weights.py
│   ├── mavt.py
│   ├── paths.py
│   └── __init__.py
│
├── notebooks/
│   ├── results_analysis.ipynb
│   └── __init__.py
│
├── scripts/
│   ├── run_pipeline.py
│   └── __init__.py
│
└── tests/
    ├── dummy_test.py
    └── __init__.py
```

---

## 📦 Installation

Clone the project:

```bash
git clone https://github.com/RomainBoinet/football-recruitment-tool.git
cd football-recruitment-tool
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> No virtual environment is required, but you may use one if desired.

---

## 🗄️ Data
Dataset source (public):  
**Football Manager 2023 Dataset** – Kaggle  
https://www.kaggle.com/datasets/platinum22/foot-ball-manager-2023-dataset  

Contains:
- **8,452 players**
- **98 attributes** (technical, physical, mental, economic)

---

## ⚽ Methodology (MAVT)

| Step | Description |
|------|-------------|
| **1. Initial Filtering** | Restrict to realistic striker profiles (position, salary, value, age). |
| **2. Scaling** | Normalize each attribute, defining maximize/minimize preferences. |
| **3. Value Functions** | Convert raw performance values into preference scores. |
| **4. Weighting** | Apply decision-maker-specific qualitative importance weights. |
| **5. Aggregation (MAVT)** | Compute overall scores for each decision-maker. |
| **6. Compromise Ranking** | Combine scores to propose balanced recommendations. |

---

## ⚖️ Compromise Approach
Instead of selecting different players for each decision-maker:
1. Compute MAVT scores for **both** decision-makers.
2. **Sum the scores** for each player.
3. Rank based on **combined performance**.

This ensures the recommendations reflect both **sporting needs** and **budget/reputation constraints**.

---

## 🏆 Final Recommended Strikers

| Player | Key Strengths |
|--------|---------------|
| **Germán Berterame** | Efficient finisher, physical presence, financially accessible |
| **Pedro Raul** | Dominant aerial ability, strong mentality profile |
| **Artem Dovbyk** | Proven scoring record, consistent performance, reasonable cost |

These players represent a **balanced compromise** between performance and financial sustainability.

---

## ▶️ Running the Pipeline

To compute rankings and generate results:

```bash
python scripts/run_pipeline.py
```

To view the final selected players in Python:

```python
import pandas as pd
from football_recruitement_tool.paths import path_to_results
df = pd.read_csv(path_to_results, sep=";", encoding="latin1")
df.head()
```

---

## 🚀 Possible Enhancements

| Improvement | Benefit |
|------------|---------|
| Add Pareto front visualization | Clearer compromise interpretation |
| Integrate real performance databases (FBref/Wyscout) | Higher decision reliability |
| Deploy Streamlit web interface | Real-world usability for scouting department |

---

## 📧 Contact
Romain BOINET 
romain.boinet56120@gmail.com
LinkedIn: https://www.linkedin.com/in/romain-boinet-5190b6265/