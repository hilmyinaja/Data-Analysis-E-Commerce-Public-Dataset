import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from babel.numbers import format_currency

sns.set(style='white')
st.set_page_config(page_title="E-Commerce Performance Dashboard", layout="wide")

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    }).reset_index()
    daily_orders_df.rename(columns={"order_id": "order_count", "payment_value": "revenue"}, inplace=True)
    return daily_orders_df

def create_sum_review_items_df(df):
    return df.groupby("product_category_name_english").review_score.mean().sort_values(ascending=False).reset_index()

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "payment_value": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    return rfm_df

# Load Data
all_df = pd.read_csv("dashboard/main_data.csv")
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

# Sidebar
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=datetime.date(2018, 12, 31), # Dikunci sampai akhir tahun 2018
        value=[min_date, max_date]
)

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

# Filter Data Berdasarkan Waktu
main_df = all_df[(all_df["order_purchase_timestamp"].dt.date >= start_date) & 
                 (all_df["order_purchase_timestamp"].dt.date <= end_date)]

# Main Dashboard
st.title('E-Commerce Analysis Dashboard')
st.caption(f"Analisis Periode: {start_date} hingga {end_date}")

# Revenue dan Order
col1, col2 = st.columns(2)
daily_orders_df = create_daily_orders_df(main_df)

with col1:
    st.metric("Total Pesanan", value=daily_orders_df.order_count.sum())
with col2:
    total_rev = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR')
    st.metric("Total Pendapatan", value=total_rev)

# Distribusi Harga & Ongkir Sesuai Feedback Reviewer
st.subheader("Distribusi Variabel Numerik")
tab1, tab2 = st.tabs(["Distribusi Harga (Price)", "Biaya Ongkir (Freight)"])

with tab1:
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    sns.histplot(main_df['price'], kde=True, ax=ax[0], color="#90CAF9")
    ax[0].set_title("Histogram Harga")
    sns.boxplot(x=main_df['price'], ax=ax[1], color="#90CAF9")
    ax[1].set_title("Boxplot Harga (Outlier Check)")
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    sns.histplot(main_df['freight_value'], kde=True, ax=ax[0], color="#FFAB91")
    ax[0].set_title("Histogram Biaya Ongkir")
    sns.boxplot(x=main_df['freight_value'], ax=ax[1], color="#FFAB91")
    ax[1].set_title("Boxplot Biaya Ongkir")
    st.pyplot(fig)

# Kualitas Produk
st.subheader("Review Score per Kategori Produk")
review_df = create_sum_review_items_df(main_df)
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="review_score", 
    y="product_category_name_english", 
    data=review_df.sort_values(by="review_score", ascending=True).head(10), 
    palette="Reds_r"
)
ax.set_title("Top 10 Kategori dengan Review Terendah", fontsize=15)
st.pyplot(fig)

# Performa Logistik
st.subheader("Logistics & Delivery Performance")
c1, c2 = st.columns(2)

with c1:
    avg_deliv = main_df.delivery_time_days.mean() if not main_df.empty else 0
    st.metric("Rata-rata Pengiriman", value=f"{avg_deliv:.2f} Hari")
with c2:
    total_obs = main_df.shape[0]
    late_rate = (main_df[main_df.delivery_diff_days > 0].shape[0] / total_obs * 100) if total_obs > 0 else 0
    st.metric("Tingkat Keterlambatan", value=f"{late_rate:.2f}%")

# RFM Analysis
st.subheader("Best Customer Based on RFM Parameters")
rfm_df = create_rfm_df(main_df)
col_r, col_f, col_m = st.columns(3)

with col_r:
    st.metric("Avg Recency", value=f"{rfm_df.recency.mean():.1f} Hari")
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette="Blues", ax=ax)
    ax.set_title("By Recency", fontsize=20)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with col_f:
    st.metric("Avg Frequency", value=f"{rfm_df.frequency.mean():.2f}")
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette="Blues", ax=ax)
    ax.set_title("By Frequency", fontsize=20)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with col_m:
    st.metric("Avg Monetary", value=format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR'))
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette="Blues", ax=ax)
    ax.set_title("By Monetary", fontsize=20)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

st.divider()
st.caption('Copyright (c) Hilmy Abid Syafi Abiyyu 2026')