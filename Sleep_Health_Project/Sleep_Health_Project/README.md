# 🌙 Sleep Health & Lifestyle Analytics Dashboard

> **An end-to-end Data Analytics & ML project** analyzing how lifestyle factors impact sleep quality and sleep disorders — built for a fresher's Data Analyst portfolio.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.20-informational)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-orange)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-green)

---

## 📌 Project Overview

This project performs a **complete data analytics pipeline** on the Sleep Health & Lifestyle dataset — from raw data exploration to a deployed interactive dashboard with machine learning predictions.

| Metric | Value |
|--------|-------|
| Dataset Size | 374 records, 13 features |
| Key Target | Sleep Disorder (None / Insomnia / Sleep Apnea) |
| Best ML Accuracy | ~92% (Random Forest / XGBoost) |
| Dashboard Pages | 7 interactive pages |

---

## 🗂️ Project Structure

```
Sleep_Health_Project/
│
├── data/
│   └── Sleep_health_and_lifestyle_dataset.csv
│
├── notebooks/
│   └── analysis.ipynb          ← Complete EDA + ML notebook
│
├── dashboard/
│   └── screenshots/            ← Dashboard screenshots
│
├── reports/
│   └── sleep_health_report.pdf ← Auto-generated report
│
├── images/                     ← All saved chart images
│
├── app.py                      ← Streamlit dashboard
├── requirements.txt            ← Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/sleep-health-analytics.git
cd sleep-health-analytics
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

### 5. Open the notebook
```bash
jupyter notebook notebooks/analysis.ipynb
```

---

## 📊 Key Findings

| Finding | Insight |
|---------|---------|
| **Stress is #1 predictor** | Correlation of -0.90 with sleep quality |
| **Obese → Sleep Apnea** | 3x higher risk than normal BMI |
| **High activity → Better sleep** | +1.8 quality points for active vs sedentary |
| **Sales roles most stressed** | Avg stress 7.8/10 vs overall 5.2/10 |
| **Insomnia profile** | Overweight + High stress + Low activity |
| **Best sleep occupation** | Engineers and Accountants |

---

## 🤖 Machine Learning Results

| Model | Accuracy | Notes |
|-------|----------|-------|
| Logistic Regression | ~87% | Good baseline |
| **Random Forest** | **~92%** | Best overall |
| XGBoost | ~91% | Close second |

**Top Features:** BMI category, Stress level, Physical activity, Systolic BP

---

## 🎛️ Dashboard Pages

1. **📊 Executive Summary** — KPI cards, disorder & BMI distribution
2. **🛌 Sleep Analysis** — Duration, quality distributions, scatter plots
3. **🏃 Lifestyle Analysis** — Activity, steps, BMI impact
4. **😰 Stress Analysis** — Stress by occupation, correlation with sleep
5. **🩺 Sleep Disorders** — Risk profiling, disorder breakdown
6. **💼 Occupation Insights** — Leaderboard, comparison charts
7. **💡 Recommendations** — Personalized risk assessment + action plan

---

## ☁️ Deployment Guide

### Deploy on Streamlit Cloud (Free)

1. Push code to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repo → `app.py` as main file
5. Click **Deploy**

### Deploy on Render (Free)

1. Create a `render.yaml` in the root:
```yaml
services:
  - type: web
    name: sleep-health-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
2. Connect your GitHub repo on render.com

---

## 📤 GitHub Upload Guide

```bash
# Initialize git
git init
git add .
git commit -m "Initial commit: Sleep Health Analytics Dashboard"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/sleep-health-analytics.git
git branch -M main
git push -u origin main
```

---

## 💼 Resume Bullet Points (ATS-Friendly)

- Developed an end-to-end Sleep Health Analytics project using Python (Pandas, Matplotlib, Seaborn, Plotly) on a 374-record dataset with 13 features
- Performed comprehensive EDA identifying stress level (r = -0.90) as the strongest predictor of poor sleep quality
- Engineered 5 new features (age groups, activity categories, stress categories) to enhance model interpretability
- Built and compared 3 ML classification models (Logistic Regression, Random Forest, XGBoost), achieving 92% accuracy in sleep disorder prediction
- Deployed a 7-page interactive Streamlit dashboard with real-time filters, KPI cards, and a personalized risk assessment engine
- Generated business insights and recommendations for HR and healthcare stakeholders based on data-driven findings

---

## 🔗 Links

- 📊 **Live Dashboard:** [Link to Streamlit Cloud]
- 💻 **GitHub Repo:** [Your Repo URL]
- 🔗 **LinkedIn Post:** [Your LinkedIn Post]

---

## 👤 Author

**[Your Name]**  
B.Tech Information Technology  
Data Analyst | Python | SQL | Tableau | Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/YOUR_USERNAME)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
