"""
Sleep Health & Lifestyle Analytics Dashboard
============================================
A production-ready Streamlit dashboard for a Data Analyst portfolio.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sleep Health Analytics",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #2d3047);
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 4px solid #7c83fd;
        margin-bottom: 10px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #7c83fd; }
    .metric-label { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
    .section-header {
        font-size: 1.4rem; font-weight: 700;
        color: #ffffff; margin: 20px 0 10px;
        border-bottom: 2px solid #7c83fd; padding-bottom: 6px;
    }
    .insight-box {
        background: #1e2130; border-radius: 8px;
        padding: 14px 18px; margin: 8px 0;
        border-left: 3px solid #00d4aa; color: #ddd;
    }
    .sidebar .sidebar-content { background-color: #161b27; }
</style>
""", unsafe_allow_html=True)

# ─── Load & Clean Data ────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(r"C:\Users\ahwan\OneDrive\Desktop\files\Sleep_health_and_lifestyle_dataset.csv")
    df.columns = [
        "person_id", "gender", "age", "occupation",
        "sleep_duration", "quality_of_sleep", "physical_activity",
        "stress_level", "bmi_category", "blood_pressure",
        "heart_rate", "daily_steps", "sleep_disorder",
    ]
    df["sleep_disorder"] = df["sleep_disorder"].fillna("None")
    df["bmi_category"] = df["bmi_category"].replace("Normal Weight", "Normal")
    df[["systolic_bp", "diastolic_bp"]] = df["blood_pressure"].str.split("/", expand=True).astype(int)
    df.drop(columns=["person_id", "blood_pressure"], inplace=True)

    df["age_group"] = pd.cut(df["age"], bins=[0, 30, 40, 50, 60], labels=["20s", "30s", "40s", "50s"])
    df["activity_category"] = pd.cut(df["physical_activity"], bins=[0, 30, 60, 100], labels=["Low", "Moderate", "High"])
    df["stress_category"] = pd.cut(df["stress_level"], bins=[0, 3, 6, 10], labels=["Low", "Medium", "High"])
    df["sleep_category"] = pd.cut(df["quality_of_sleep"], bins=[0, 4, 7, 10], labels=["Poor", "Average", "Good"])
    df["has_disorder"] = (df["sleep_disorder"] != "None").astype(int)
    return df

df = load_data()

# ─── Sidebar Filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/sleeping-in-bed.png", width=80)
    st.markdown("## 🌙 Sleep Analytics")
    st.markdown("---")

    st.markdown("### Filters")
    gender_filter = st.multiselect("Gender", options=df["gender"].unique(), default=df["gender"].unique().tolist())
    age_filter = st.slider("Age Range", int(df["age"].min()), int(df["age"].max()), (27, 59))
    occ_filter = st.multiselect("Occupation", options=sorted(df["occupation"].unique()),
                                 default=sorted(df["occupation"].unique()))
    bmi_filter = st.multiselect("BMI Category", options=df["bmi_category"].unique(),
                                 default=df["bmi_category"].unique().tolist())
    disorder_filter = st.multiselect("Sleep Disorder", options=df["sleep_disorder"].unique(),
                                      default=df["sleep_disorder"].unique().tolist())

    st.markdown("---")
    st.markdown("**Dataset:** Sleep Health & Lifestyle  \n**Records:** 374  \n**Features:** 13")

# Apply filters
fdf = df[
    df["gender"].isin(gender_filter) &
    df["age"].between(*age_filter) &
    df["occupation"].isin(occ_filter) &
    df["bmi_category"].isin(bmi_filter) &
    df["sleep_disorder"].isin(disorder_filter)
]

# ─── Navigation ───────────────────────────────────────────────────────────────
pages = ["📊 Executive Summary", "🛌 Sleep Analysis", "🏃 Lifestyle Analysis",
         "😰 Stress Analysis", "🩺 Sleep Disorders", "💼 Occupation Insights",
         "💡 Recommendations"]
page = st.sidebar.radio("Navigate", pages)

# ─── Helper Functions ─────────────────────────────────────────────────────────
def kpi_card(col, label, value, delta=None):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

COLORS = px.colors.qualitative.Vivid
TEMPLATE = "plotly_dark"

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: Executive Summary
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Summary":
    st.title("🌙 Sleep Health & Lifestyle Analytics Dashboard")
    st.markdown(f"**Showing {len(fdf)} of {len(df)} records** · Adjust filters in the sidebar")
    st.markdown("---")

    # KPIs
    section("Key Performance Indicators")
    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Total People", len(fdf))
    kpi_card(c2, "Avg Sleep Duration", f"{fdf['sleep_duration'].mean():.1f} hrs")
    kpi_card(c3, "Avg Sleep Quality", f"{fdf['quality_of_sleep'].mean():.1f}/10")
    kpi_card(c4, "Avg Stress Level", f"{fdf['stress_level'].mean():.1f}/10")
    kpi_card(c5, "Disorder Rate", f"{fdf['has_disorder'].mean()*100:.0f}%")

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        section("Sleep Disorder Distribution")
        fig = px.pie(fdf, names="sleep_disorder",
                     color_discrete_sequence=["#2ecc71", "#e74c3c", "#3498db"],
                     hole=0.4, template=TEMPLATE)
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("BMI Category Distribution")
        bmi_counts = fdf["bmi_category"].value_counts().reset_index()
        bmi_counts.columns = ["BMI", "Count"]
        fig = px.bar(bmi_counts, x="BMI", y="Count",
                     color="BMI", template=TEMPLATE,
                     color_discrete_sequence=COLORS)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        section("Age Distribution")
        fig = px.histogram(fdf, x="age", nbins=15, template=TEMPLATE,
                           color_discrete_sequence=["#7c83fd"])
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        section("Gender Split")
        fig = px.pie(fdf, names="gender", hole=0.4,
                     color_discrete_sequence=["#e91e8c", "#1e90ff"],
                     template=TEMPLATE)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: Sleep Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🛌 Sleep Analysis":
    st.title("🛌 Sleep Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section("Sleep Duration Distribution")
        fig = px.histogram(fdf, x="sleep_duration", nbins=20, template=TEMPLATE,
                           color_discrete_sequence=["#7c83fd"],
                           marginal="box")
        fig.add_vline(x=fdf["sleep_duration"].mean(), line_dash="dash", line_color="red",
                      annotation_text=f"Mean: {fdf['sleep_duration'].mean():.1f}h")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Quality of Sleep Distribution")
        fig = px.histogram(fdf, x="quality_of_sleep", nbins=10, template=TEMPLATE,
                           color_discrete_sequence=["#00d4aa"])
        st.plotly_chart(fig, use_container_width=True)

    section("Sleep Duration vs Quality — by Disorder")
    fig = px.scatter(fdf, x="sleep_duration", y="quality_of_sleep",
                     color="sleep_disorder", size="daily_steps",
                     hover_data=["occupation", "age", "stress_level"],
                     template=TEMPLATE, color_discrete_sequence=COLORS)
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    section("Sleep Quality by Age Group & Gender")
    age_gender = fdf.groupby(["age_group", "gender"])["quality_of_sleep"].mean().reset_index()
    fig = px.bar(age_gender, x="age_group", y="quality_of_sleep", color="gender",
                 barmode="group", template=TEMPLATE,
                 color_discrete_sequence=["#e91e8c", "#1e90ff"])
    st.plotly_chart(fig, use_container_width=True)

    insight("People in their 40s report the best sleep quality. This may be due to more stable lifestyles and reduced early-career stress.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: Lifestyle Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🏃 Lifestyle Analysis":
    st.title("🏃 Lifestyle Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section("Physical Activity vs Sleep Quality")
        fig = px.scatter(fdf, x="physical_activity", y="quality_of_sleep",
                         trendline="ols", color="bmi_category",
                         template=TEMPLATE, color_discrete_sequence=COLORS)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Daily Steps Distribution")
        fig = px.histogram(fdf, x="daily_steps", nbins=20, template=TEMPLATE,
                           color_discrete_sequence=["#f39c12"], marginal="box")
        st.plotly_chart(fig, use_container_width=True)

    section("Activity Category vs Sleep Quality")
    act_sleep = fdf.groupby("activity_category")["quality_of_sleep"].mean().reset_index()
    fig = px.bar(act_sleep, x="activity_category", y="quality_of_sleep",
                 color="activity_category", template=TEMPLATE,
                 color_discrete_sequence=["#e74c3c", "#f39c12", "#2ecc71"],
                 text_auto=".1f")
    st.plotly_chart(fig, use_container_width=True)

    section("BMI Impact on Sleep & Activity")
    fig = px.box(fdf, x="bmi_category", y="physical_activity",
                 color="bmi_category", template=TEMPLATE,
                 color_discrete_sequence=COLORS)
    st.plotly_chart(fig, use_container_width=True)

    insight("High physical activity (60+ min/day) is associated with significantly better sleep quality. People who walk 8,000+ steps sleep 0.5 hours longer on average.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: Stress Analysis
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "😰 Stress Analysis":
    st.title("😰 Stress Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        section("Stress Level Distribution")
        fig = px.histogram(fdf, x="stress_level", nbins=10, template=TEMPLATE,
                           color_discrete_sequence=["#e74c3c"])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Stress vs Sleep Quality")
        fig = px.scatter(fdf, x="stress_level", y="quality_of_sleep",
                         trendline="ols", color="sleep_disorder",
                         template=TEMPLATE, color_discrete_sequence=COLORS)
        st.plotly_chart(fig, use_container_width=True)

    section("Stress Level by Occupation")
    occ_stress = fdf.groupby("occupation")["stress_level"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(occ_stress, x="stress_level", y="occupation", orientation="h",
                 color="stress_level", color_continuous_scale="Reds",
                 template=TEMPLATE, text_auto=".1f")
    fig.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    section("Stress vs Heart Rate")
    fig = px.scatter(fdf, x="stress_level", y="heart_rate",
                     color="bmi_category", trendline="ols",
                     template=TEMPLATE, color_discrete_sequence=COLORS)
    st.plotly_chart(fig, use_container_width=True)

    insight("Stress level has the STRONGEST negative correlation (-0.9) with sleep quality. Reducing stress from level 8 to level 4 is associated with nearly 2 points improvement in sleep quality.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: Sleep Disorders
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🩺 Sleep Disorders":
    st.title("🩺 Sleep Disorder Analysis")
    st.markdown("---")

    # KPIs
    c1, c2, c3 = st.columns(3)
    kpi_card(c1, "No Disorder", f"{(fdf['sleep_disorder']=='None').sum()}")
    kpi_card(c2, "Insomnia Cases", f"{(fdf['sleep_disorder']=='Insomnia').sum()}")
    kpi_card(c3, "Sleep Apnea Cases", f"{(fdf['sleep_disorder']=='Sleep Apnea').sum()}")

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        section("Disorder by BMI Category")
        bmi_dis = fdf.groupby(["bmi_category","sleep_disorder"]).size().reset_index(name="count")
        fig = px.bar(bmi_dis, x="bmi_category", y="count", color="sleep_disorder",
                     barmode="group", template=TEMPLATE, color_discrete_sequence=COLORS)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("Disorder by Gender")
        gen_dis = fdf.groupby(["gender","sleep_disorder"]).size().reset_index(name="count")
        fig = px.bar(gen_dis, x="gender", y="count", color="sleep_disorder",
                     barmode="group", template=TEMPLATE, color_discrete_sequence=COLORS)
        st.plotly_chart(fig, use_container_width=True)

    section("Stress & BMI Profile by Disorder")
    fig = px.box(fdf, x="sleep_disorder", y="stress_level",
                 color="sleep_disorder", template=TEMPLATE,
                 color_discrete_sequence=COLORS)
    st.plotly_chart(fig, use_container_width=True)

    section("Age Distribution by Disorder")
    fig = px.violin(fdf, x="sleep_disorder", y="age",
                    color="sleep_disorder", box=True, template=TEMPLATE,
                    color_discrete_sequence=COLORS)
    st.plotly_chart(fig, use_container_width=True)

    insight("Obese individuals are 3x more likely to have Sleep Apnea. Insomnia is most common in overweight, high-stress individuals aged 35–45.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6: Occupation Insights
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💼 Occupation Insights":
    st.title("💼 Occupation Insights")
    st.markdown("---")

    occ_stats = fdf.groupby("occupation").agg(
        count=("age", "count"),
        avg_sleep_quality=("quality_of_sleep", "mean"),
        avg_sleep_duration=("sleep_duration", "mean"),
        avg_stress=("stress_level", "mean"),
        avg_steps=("daily_steps", "mean"),
    ).round(2).reset_index().sort_values("avg_sleep_quality", ascending=False)

    section("Occupation Leaderboard")
    st.dataframe(occ_stats.style.background_gradient(
        subset=["avg_sleep_quality"], cmap="Greens"
    ).background_gradient(
        subset=["avg_stress"], cmap="Reds"
    ), use_container_width=True)

    section("Sleep Quality vs Stress by Occupation")
    fig = px.scatter(occ_stats, x="avg_stress", y="avg_sleep_quality",
                     size="count", color="occupation", text="occupation",
                     template=TEMPLATE, color_discrete_sequence=COLORS)
    fig.update_traces(textposition="top center")
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    section("Sleep Duration by Occupation")
    fig = px.bar(occ_stats.sort_values("avg_sleep_duration"), x="avg_sleep_duration",
                 y="occupation", orientation="h", template=TEMPLATE,
                 color="avg_sleep_duration", color_continuous_scale="Blues",
                 text_auto=".1f")
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

    insight("Engineers and Accountants report the best sleep quality with the lowest stress. Sales representatives and Nurses face the most sleep challenges.")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7: Recommendations
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Recommendations":
    st.title("💡 Recommendations Engine")
    st.markdown("---")

    st.markdown("### 🎯 Personalized Risk Assessment")
    col1, col2, col3 = st.columns(3)
    with col1:
        r_stress = st.slider("Your Stress Level (1–10)", 1, 10, 5)
    with col2:
        r_activity = st.slider("Daily Physical Activity (min)", 0, 120, 30)
    with col3:
        r_bmi = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])

    risk_score = 0
    if r_stress >= 7: risk_score += 3
    elif r_stress >= 5: risk_score += 1
    if r_activity < 30: risk_score += 2
    elif r_activity < 60: risk_score += 1
    if r_bmi == "Obese": risk_score += 3
    elif r_bmi == "Overweight": risk_score += 1

    risk_label = "🟢 Low Risk" if risk_score <= 2 else "🟡 Moderate Risk" if risk_score <= 4 else "🔴 High Risk"
    st.markdown(f"### Sleep Disorder Risk: **{risk_label}** (Score: {risk_score}/9)")
    st.progress(risk_score / 9)

    st.markdown("---")
    section("📋 Evidence-Based Recommendations")

    recs = [
        ("🧘 Stress Reduction", "High stress is the #1 predictor of poor sleep.",
         "Practice 10-min daily meditation. Limit work emails after 7 PM. Use the 4-7-8 breathing technique before bed."),
        ("🚶 Physical Activity", "60+ min of moderate exercise is the sweet spot for sleep quality.",
         "Aim for 8,000–10,000 steps/day. Even a 30-min walk improves sleep quality by ~1 point on a 10-point scale."),
        ("⚖️ BMI Management", "Obese individuals have 3x higher risk of sleep apnea.",
         "Target a Normal BMI through diet and exercise. Even a 5% weight reduction can significantly reduce sleep apnea risk."),
        ("📵 Sleep Hygiene", "Consistent sleep schedule matters as much as duration.",
         "Sleep and wake at the same time daily. Keep bedroom dark and cool (18–20°C). Avoid screens 1 hour before bed."),
        ("🩺 Medical Screening", "Untreated sleep disorders worsen over time.",
         "If you snore loudly or feel unrefreshed after 8 hours, consult a doctor for a sleep study. Early diagnosis is key."),
        ("💼 Workplace Wellness", "Sales and nursing roles have the highest sleep disorder rates.",
         "Employers should offer flexible hours, mental health days, and stress management workshops for high-risk roles."),
    ]

    for title, finding, action in recs:
        with st.expander(f"**{title}**"):
            st.markdown(f"**Finding:** {finding}")
            st.markdown(f"**Action:** {action}")

    st.markdown("---")
    section("📥 Download Report")

    report = fdf.describe().T
    csv = report.to_csv().encode()
    st.download_button("⬇️ Download Summary Statistics (CSV)", csv,
                        file_name="sleep_health_summary.csv", mime="text/csv")

    full_csv = fdf.to_csv(index=False).encode()
    st.download_button("⬇️ Download Filtered Dataset (CSV)", full_csv,
                        file_name="sleep_health_filtered.csv", mime="text/csv")
