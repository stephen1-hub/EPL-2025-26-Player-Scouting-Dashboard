# ⚽ EPL 2025/26 Player Scouting Dashboard

An interactive football analytics dashboard built with **Python** and **Streamlit** to evaluate player performance in the English Premier League using expected goals (xG) and expected assists (xA).

---

## 🚀 Overview

This project simulates a **data-driven scouting tool** used by football clubs to:

- Identify high-impact players  
- Detect undervalued talent (hidden gems)  
- Analyze finishing efficiency  
- Measure team dependency on individual players  

---

## 📊 Key Features

### ⚡ Player Performance
- xG, xA, goals, and assists
- Per 90 metrics (xG90, xA90)

### 🎯 Finishing Analysis
- Compare goals vs expected goals
- Identify overperformers and underperformers

### 💎 Hidden Gems
- Low minutes + high output players
- Potential breakout candidates

### 🏗️ Team Dependency
- % contribution to team attacking output
- Identify system-critical players

### ⚖️ Role Profiling
- Scorer vs creator analysis (xG vs xA)

---

## 🧠 Key Insight

> A small number of players generate a disproportionately large share of attacking output in the EPL, highlighting both their importance and the structural risk of over-dependence.

---

## 🛠️ Tech Stack

- Python  
- Pandas  
- Streamlit  
- Matplotlib  

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
