import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Energy Price Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("DATA/data/final_dataset.csv")
df["time"] = pd.to_datetime(df["time"])

# ---------------- FEATURES ----------------
df["renewable_ratio"] = (df["wind"] + df["solar"]) / df["load"]
df["price_spike"] = df["price"] > df["price"].quantile(0.9)

# ---------------- MODEL ----------------
X = df[["load", "wind", "solar"]]
y = df["price"]

model = LinearRegression()
model.fit(X, y)

# ---------------- HEADER ----------------
st.title("⚡ German Electricity Price Dashboard")
st.markdown("Analyze and predict electricity prices based on demand and renewable energy")

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Price", f"{df['price'].mean():.2f} €/MWh")
col2.metric("Max Price", f"{df['price'].max():.2f} €/MWh")
col3.metric("Spike Rate", f"{df['price_spike'].mean()*100:.1f}%")

# ---------------- INPUTS ----------------
st.sidebar.header("🔧 Input Parameters")

load = st.sidebar.slider("Demand (MWh)", int(df["load"].min()), int(df["load"].max()))
wind = st.sidebar.slider("Wind (MWh)", int(df["wind"].min()), int(df["wind"].max()))
solar = st.sidebar.slider("Solar (MWh)", int(df["solar"].min()), int(df["solar"].max()))

# ---------------- PREDICTION ----------------
prediction = model.predict([[load, wind, solar]])[0]

st.subheader("💰 Predicted Price")

if prediction > df["price"].quantile(0.9):
    st.error(f"⚠️ High Price Spike: {prediction:.2f} €/MWh")
else:
    st.success(f"Predicted Price: {prediction:.2f} €/MWh")

# ---------------- GRAPHS ----------------
col1, col2 = st.columns(2)

# Price Trend
with col1:
    st.subheader("📊 Price Trend")
    fig, ax = plt.subplots()
    ax.plot(df["time"], df["price"])
    ax.set_title("Electricity Price Over Time")
    st.pyplot(fig)

# Renewable Impact
with col2:
    st.subheader("🌱 Renewable Impact")
    fig, ax = plt.subplots()
    ax.scatter(df["renewable_ratio"], df["price"])
    ax.set_xlabel("Renewable Share")
    ax.set_ylabel("Price")
    st.pyplot(fig)

# ---------------- INSIGHTS ----------------
st.subheader("🧠 Key Insights")

st.markdown("""
- Electricity prices increase with demand  
- Higher renewable energy reduces electricity prices  
- Price spikes occur during high demand and low renewable generation  
""")