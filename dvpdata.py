import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Retail Sales Dashboard", page_icon="🛒", layout="wide")

# Title of the Dashboard
st.title("🛒 Interactive Retail Sales Dashboard")
st.markdown("Explore your retail sales data with interactive filters and charts.")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("retail_sales_dataset.csv")
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    # Extract Month-Year for easier time-series grouping
    df['Month-Year'] = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# =======================
# Sidebar: Filters
# =======================
st.sidebar.header("Filter Data")

# 1. Date Range Filter
min_date = df['Date'].min().date()
max_date = df['Date'].min().date()
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=[df['Date'].min().date(), df['Date'].max().date()],
    min_value=df['Date'].min().date(),
    max_value=df['Date'].max().date()
)

# 2. Product Category Filter
categories = st.sidebar.multiselect(
    "Select Product Category",
    options=df["Product Category"].unique(),
    default=df["Product Category"].unique()
)

# 3. Gender Filter
genders = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Apply Filters
filtered_df = df[
    (df['Date'].dt.date >= start_date) & 
    (df['Date'].dt.date <= end_date) & 
    (df['Product Category'].isin(categories)) &
    (df['Gender'].isin(genders))
]

# =======================
# Main Area: KPIs
# =======================
st.markdown("### Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Total Amount"].sum()
total_transactions = filtered_df["Transaction ID"].nunique()
total_items_sold = filtered_df["Quantity"].sum()
avg_transaction = filtered_df["Total Amount"].mean() if total_transactions > 0 else 0

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Transactions", f"{total_transactions}")
col3.metric("Items Sold", f"{total_items_sold}")
col4.metric("Avg Transaction Value", f"${avg_transaction:,.2f}")

st.divider()

# =======================
# Main Area: Charts
# =======================
colA, colB = st.columns(2)

# Chart 1: Sales over Time
with colA:
    st.subheader("Sales Over Time")
    sales_over_time = filtered_df.groupby("Date")["Total Amount"].sum().reset_index()
    fig_time = px.line(sales_over_time, x="Date", y="Total Amount", 
                       labels={"Total Amount": "Daily Sales ($)"},
                       template="plotly_white")
    st.plotly_chart(fig_time, use_container_width=True)

# Chart 2: Sales by Product Category
with colB:
    st.subheader("Sales by Category")
    sales_by_cat = filtered_df.groupby("Product Category")["Total Amount"].sum().reset_index()
    fig_cat = px.bar(sales_by_cat, x="Product Category", y="Total Amount", 
                     color="Product Category", template="plotly_white")
    st.plotly_chart(fig_cat, use_container_width=True)

colC, colD = st.columns(2)

# Chart 3: Sales by Gender
with colC:
    st.subheader("Sales Proportion by Gender")
    sales_by_gender = filtered_df.groupby("Gender")["Total Amount"].sum().reset_index()
    fig_gender = px.pie(sales_by_gender, names="Gender", values="Total Amount", hole=0.4)
    st.plotly_chart(fig_gender, use_container_width=True)

# Chart 4: Customer Age Distribution
with colD:
    st.subheader("Customer Age Distribution")
    fig_age = px.histogram(filtered_df, x="Age", nbins=20, 
                           color_discrete_sequence=["#0083B8"], 
                           template="plotly_white")
    st.plotly_chart(fig_age, use_container_width=True)

# Data Table
st.divider()
st.subheader("Raw Data View")
st.dataframe(filtered_df.drop(columns=["Month-Year"]))
#to run the app, use the command: python -m streamlit run dvpdata.py