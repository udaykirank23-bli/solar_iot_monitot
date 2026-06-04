import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import boto3
from decimal import Decimal
import json

# Page config
st.set_page_config(
    page_title="Solar Plant Monitor",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Solar Plant IoT Monitor")
st.markdown("Real-time fault detection dashboard — powered by AWS IoT + ML")

# Load data from processed CSV
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed_data.csv')
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'])
    return df

df = load_data()

# --- KPI Cards ---
col1, col2, col3, col4 = st.columns(4)

total = len(df)
faults = len(df[df['ANOMALY'] == -1])
normal = len(df[df['ANOMALY'] == 1])
avg_pr = df['PERFORMANCE_RATIO'].mean()

col1.metric("Total Readings", f"{total:,}")
col2.metric("Normal Readings", f"{normal:,}")
col3.metric("Faults Detected", f"{faults:,}", delta=f"{faults/total*100:.1f}%", delta_color="inverse")
col4.metric("Avg Performance Ratio", f"{avg_pr:.2f}")

st.divider()

# --- Power Output Over Time ---
st.subheader("⚡ AC Power Output Over Time")
fig1, ax1 = plt.subplots(figsize=(12, 4))
colors = df['ANOMALY'].map({1: 'blue', -1: 'red'})
ax1.scatter(df['DATE_TIME'], df['AC_POWER'], c=colors, s=1, alpha=0.5)
ax1.set_xlabel("Date")
ax1.set_ylabel("AC Power (W)")
ax1.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', label='Normal'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Fault')
])
st.pyplot(fig1)

st.divider()

# --- Performance Ratio Chart ---
st.subheader("📊 Performance Ratio Over Time")
fig2, ax2 = plt.subplots(figsize=(12, 4))
ax2.scatter(df['DATE_TIME'], df['PERFORMANCE_RATIO'], c=colors, s=1, alpha=0.5)
ax2.set_xlabel("Date")
ax2.set_ylabel("Performance Ratio")
ax2.axhline(y=df['PERFORMANCE_RATIO'].quantile(0.05), color='orange', linestyle='--', label='Fault threshold')
ax2.legend()
st.pyplot(fig2)

st.divider()

# --- Fault Records Table ---
st.subheader("🚨 Recent Fault Records")
faults_df = df[df['ANOMALY'] == -1][['DATE_TIME', 'SOURCE_KEY', 'AC_POWER', 'PERFORMANCE_RATIO', 'DC_AC_EFFICIENCY']].head(20)
faults_df.columns = ['Timestamp', 'Inverter ID', 'AC Power (W)', 'Performance Ratio', 'DC/AC Efficiency']
st.dataframe(faults_df, use_container_width=True)

st.divider()

# --- Inverter Summary ---
st.subheader("🔌 Fault Count by Inverter")
fault_by_inverter = df[df['ANOMALY'] == -1].groupby('SOURCE_KEY').size().reset_index(name='Fault Count')
fault_by_inverter = fault_by_inverter.sort_values('Fault Count', ascending=False)
st.bar_chart(fault_by_inverter.set_index('SOURCE_KEY'))