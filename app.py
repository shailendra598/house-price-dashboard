import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="House Price Dashboard", layout="wide")

# Title
st.title("🏠 House Price Analysis Dashboard")

# Load dataset
df = pd.read_csv("train.csv")

# ================= Sidebar =================
st.sidebar.header("🔎 Filter Options")

# Quality filter
selected_quality = st.sidebar.multiselect(
    "Select Overall Quality:",
    options=sorted(df["OverallQual"].unique()),
    default=sorted(df["OverallQual"].unique())
)

# Price range filter
price_range = st.sidebar.slider(
    "Select Price Range:",
    int(df["SalePrice"].min()),
    int(df["SalePrice"].max()),
    (
        int(df["SalePrice"].min()),
        int(df["SalePrice"].max())
    )
)

# Apply filters
filtered_df = df[
    (df["OverallQual"].isin(selected_quality)) &
    (df["SalePrice"] >= price_range[0]) &
    (df["SalePrice"] <= price_range[1])
]

# ================= Metrics =================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Houses", filtered_df.shape[0])
col2.metric("Average Price", f"${int(filtered_df['SalePrice'].mean())}")
col3.metric("Median Price", f"${int(filtered_df['SalePrice'].median())}")

# ================= Price Distribution =================
st.subheader("📈 Sale Price Distribution")

fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["SalePrice"], bins=30, kde=True, ax=ax1)
st.pyplot(fig1)

# ================= Living Area vs Price =================
st.subheader("📐 Price vs Living Area")

fig2, ax2 = plt.subplots()
sns.scatterplot(
    x="GrLivArea",
    y="SalePrice",
    data=filtered_df,
    ax=ax2
)
st.pyplot(fig2)

# ================= Neighborhood Analysis =================
st.subheader("🏘 Average Price by Neighborhood")

neigh_price = (
    filtered_df
    .groupby("Neighborhood")["SalePrice"]
    .mean()
    .sort_values(ascending=False)
)

fig3, ax3 = plt.subplots(figsize=(10, 5))
neigh_price.plot(kind="bar", ax=ax3)
plt.xticks(rotation=90)
st.pyplot(fig3)

# ================= Footer =================
st.markdown("---")
st.markdown("✅ Built using Streamlit | Kaggle House Prices Dataset")
