import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📊 Employee Engagement & Burnout Dashboard")

# Load data
df = pd.read_csv("Palo Alto Networks.csv")

# Preprocess
df['OverTime'] = df['OverTime'].map({'Yes': 1, 'No': 0})

# Engagement Index
df['EngagementIndex'] = (
    df['JobInvolvement'] +
    df['JobSatisfaction'] +
    df['EnvironmentSatisfaction'] +
    df['RelationshipSatisfaction']
) / 4

# Burnout Risk
def risk(row):
    if row['OverTime'] == 1 and row['WorkLifeBalance'] <= 2:
        return 'High'
    elif row['OverTime'] == 1 or row['WorkLifeBalance'] <= 2:
        return 'Medium'
    else:
        return 'Low'

df['BurnoutRisk'] = df.apply(risk, axis=1)

# =========================
# 🎛️ SIDEBAR FILTERS
# =========================

st.sidebar.header("🔍 Filters")

department = st.sidebar.selectbox(
    "Select Department",
    ["All"] + list(df['Department'].unique())
)

overtime = st.sidebar.selectbox(
    "Overtime",
    ["All", "Yes", "No"]
)

# Apply filters
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[filtered_df['Department'] == department]

if overtime != "All":
    val = 1 if overtime == "Yes" else 0
    filtered_df = filtered_df[filtered_df['OverTime'] == val]

# =========================
# 📌 KPI SECTION
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Engagement", round(filtered_df['EngagementIndex'].mean(), 2))
col2.metric("High Burnout", (filtered_df['BurnoutRisk'] == 'High').sum())
col3.metric("Attrition", filtered_df['Attrition'].sum())
col4.metric("Avg Work-Life Balance", round(filtered_df['WorkLifeBalance'].mean(), 2))

st.divider()

# =========================
# 📊 VISUALS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Burnout Risk Distribution")
    st.bar_chart(filtered_df['BurnoutRisk'].value_counts())

with col2:
    st.subheader("⏱️ Overtime vs Engagement")
    st.bar_chart(filtered_df.groupby('OverTime')['EngagementIndex'].mean())

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("💔 Engagement vs Attrition")
    st.bar_chart(filtered_df.groupby('Attrition')['EngagementIndex'].mean())

with col4:
    st.subheader("🌍 Travel vs Engagement")
    st.bar_chart(filtered_df.groupby('BusinessTravel')['EngagementIndex'].mean())

st.divider()

# =========================
# 🧠 MANAGER ACTION PANEL
# =========================

st.subheader("🚨 Manager Action Panel")

high_risk = filtered_df[filtered_df['BurnoutRisk'] == 'High']

st.write("High Risk Employees:", len(high_risk))

st.dataframe(
    high_risk[['Department', 'JobRole', 'WorkLifeBalance', 'OverTime', 'EngagementIndex']]
)