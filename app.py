import os

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lulu Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#1F6F50"
ACCENT = "#F2A93B"

# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    return df


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "lulu_sales_data.csv")

if not os.path.exists(DATA_PATH):
    st.error(
        "Data file not found at `data/lulu_sales_data.csv`.\n\n"
        "This usually means the `data/` folder wasn't pushed to GitHub, or "
        "the file was renamed. In your repo, confirm the file exists at "
        "exactly that path (case-sensitive), then redeploy. "
        f"\n\nLooked in: `{DATA_PATH}`"
    )
    st.stop()

df = load_data(DATA_PATH)

# ----------------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------------
st.sidebar.title("🛒 Lulu Sales Dashboard")
st.sidebar.caption("Filter the data to explore performance")

min_date, max_date = df["Order_Date"].min().date(), df["Order_Date"].max().date()
date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

cities = sorted(df["City"].unique())
sel_cities = st.sidebar.multiselect("City", cities, default=cities)

stores = sorted(df[df["City"].isin(sel_cities)]["Store_Name"].unique())
sel_stores = st.sidebar.multiselect("Store", stores, default=stores)

categories = sorted(df["Category"].unique())
sel_categories = st.sidebar.multiselect("Category", categories, default=categories)

channels = sorted(df["Sales_Channel"].unique())
sel_channels = st.sidebar.multiselect("Sales Channel", channels, default=channels)

st.sidebar.markdown("---")
st.sidebar.caption("Synthetic data for classroom / stakeholder demo purposes.")

# ----------------------------------------------------------------------------
# Apply filters
# ----------------------------------------------------------------------------
mask = (
    (df["Order_Date"].dt.date >= start_date)
    & (df["Order_Date"].dt.date <= end_date)
    & (df["City"].isin(sel_cities))
    & (df["Store_Name"].isin(sel_stores))
    & (df["Category"].isin(sel_categories))
    & (df["Sales_Channel"].isin(sel_channels))
)
fdf = df.loc[mask].copy()

if fdf.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ----------------------------------------------------------------------------
# Header + KPIs
# ----------------------------------------------------------------------------
st.title("Lulu Hypermarket — Sales Performance Dashboard")
st.caption(f"Showing {len(fdf):,} orders from {start_date} to {end_date}")

total_orders = fdf["Order_ID"].nunique()
total_qty = int(fdf["Quantity"].sum())
net_sales = fdf["Net_Amount_AED"].sum()
profit = fdf["Profit_AED"].sum()
aov = fdf["Net_Amount_AED"].mean()
margin = profit / net_sales if net_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Orders", f"{total_orders:,}")
k2.metric("Units Sold", f"{total_qty:,}")
k3.metric("Net Sales (AED)", f"{net_sales:,.0f}")
k4.metric("Profit (AED)", f"{profit:,.0f}")
k5.metric("Profit Margin", f"{margin:.1%}")

st.markdown("---")

# ----------------------------------------------------------------------------
# Row 1: Sales trend + Category breakdown
# ----------------------------------------------------------------------------
c1, c2 = st.columns((2, 1))

with c1:
    st.subheader("Net Sales Trend Over Time")
    trend_freq = st.radio("Aggregate by", ["Day", "Week", "Month"], horizontal=True, index=2)
    freq_map = {"Day": "D", "Week": "W", "Month": "MS"}
    trend = (
        fdf.set_index("Order_Date")
        .resample(freq_map[trend_freq])["Net_Amount_AED"]
        .sum()
        .reset_index()
    )
    fig_trend = px.line(
        trend, x="Order_Date", y="Net_Amount_AED", markers=True,
        color_discrete_sequence=[PRIMARY],
    )
    fig_trend.update_layout(
        yaxis_title="Net Sales (AED)", xaxis_title="", margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with c2:
    st.subheader("Sales by Category")
    cat_sales = (
        fdf.groupby("Category")["Net_Amount_AED"].sum().sort_values(ascending=False).reset_index()
    )
    fig_cat = px.pie(
        cat_sales, names="Category", values="Net_Amount_AED", hole=0.45,
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )
    fig_cat.update_layout(margin=dict(t=10, b=10))
    st.plotly_chart(fig_cat, use_container_width=True)

# ----------------------------------------------------------------------------
# Row 2: Store comparison + Top products
# ----------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Net Sales by Store")
    store_sales = (
        fdf.groupby("Store_Name")["Net_Amount_AED"].sum().sort_values().reset_index()
    )
    fig_store = px.bar(
        store_sales, x="Net_Amount_AED", y="Store_Name", orientation="h",
        color_discrete_sequence=[ACCENT],
    )
    fig_store.update_layout(
        xaxis_title="Net Sales (AED)", yaxis_title="", margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_store, use_container_width=True)

with c4:
    st.subheader("Top 10 Products by Net Sales")
    top_products = (
        fdf.groupby("Product")["Net_Amount_AED"].sum().sort_values(ascending=False).head(10).reset_index()
    )
    fig_top = px.bar(
        top_products.sort_values("Net_Amount_AED"),
        x="Net_Amount_AED", y="Product", orientation="h",
        color_discrete_sequence=[PRIMARY],
    )
    fig_top.update_layout(
        xaxis_title="Net Sales (AED)", yaxis_title="", margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ----------------------------------------------------------------------------
# Row 3: Payment method + Channel
# ----------------------------------------------------------------------------
c5, c6 = st.columns(2)

with c5:
    st.subheader("Orders by Payment Method")
    pay = fdf["Payment_Method"].value_counts().reset_index()
    pay.columns = ["Payment_Method", "Orders"]
    fig_pay = px.bar(
        pay, x="Payment_Method", y="Orders", color_discrete_sequence=[ACCENT]
    )
    fig_pay.update_layout(xaxis_title="", margin=dict(t=10, b=10))
    st.plotly_chart(fig_pay, use_container_width=True)

with c6:
    st.subheader("Sales by Channel")
    chan = fdf.groupby("Sales_Channel")["Net_Amount_AED"].sum().reset_index()
    fig_chan = px.bar(
        chan, x="Sales_Channel", y="Net_Amount_AED",
        color_discrete_sequence=[PRIMARY],
    )
    fig_chan.update_layout(xaxis_title="", yaxis_title="Net Sales (AED)", margin=dict(t=10, b=10))
    st.plotly_chart(fig_chan, use_container_width=True)

# ----------------------------------------------------------------------------
# Data table + download
# ----------------------------------------------------------------------------
st.markdown("---")
st.subheader("Transaction-Level Data")
st.dataframe(fdf.sort_values("Order_Date", ascending=False), use_container_width=True, height=350)

csv = fdf.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download filtered data as CSV",
    data=csv,
    file_name="lulu_sales_filtered.csv",
    mime="text/csv",
)
