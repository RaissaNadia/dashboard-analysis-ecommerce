# 1. IMPORT
import streamlit as st
import pandas as pd
import os
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "main_data.csv")

    if not os.path.exists(file_path):
        st.error(f"File tidak ditemukan: {file_path}")
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['year'] = df['order_purchase_timestamp'].dt.year
    df['month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    return df

df = load_data()

if df.empty:
    st.stop()

# SIDEBAR
st.sidebar.title("🔎 Filter")

year = st.sidebar.multiselect(
    "Tahun",
    sorted(df['year'].unique()),
    default=sorted(df['year'].unique())
)

state = st.sidebar.multiselect(
    "State",
    sorted(df['customer_state'].unique()),
    default=sorted(df['customer_state'].unique())
)

df_filtered = df[
    (df['year'].isin(year)) &
    (df['customer_state'].isin(state))
]

# KPI
st.title("📊 Dashboard Analisis E-Commerce")

k1, k2, k3, k4 = st.columns(4)

k1.metric("💰 Revenue", f"{df_filtered['revenue'].sum():,.0f}")
k2.metric("📦 Orders", df_filtered['order_id'].nunique())
k3.metric("⭐ Review", f"{df_filtered['review_score'].mean():.2f}")
k4.metric("🚚 Late %", f"{df_filtered['is_late'].mean()*100:.2f}%")

# TREND
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trend")
    monthly = df_filtered.groupby('month')['revenue'].sum().reset_index()
    fig = px.line(monthly, x='month', y='revenue', height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏆 Top Produk (Transaksi)")
    top_product = df_filtered.groupby('product_category_name_english')['order_id'] \
        .count().sort_values(ascending=False).head(10)
    fig = px.bar(top_product, x=top_product.values, y=top_product.index,
                 orientation='h', height=350)
    st.plotly_chart(fig, use_container_width=True)

# TOP PRODUK
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Top Produk (Revenue)")
    top_rev = df_filtered.groupby('product_category_name_english')['revenue'] \
        .sum().sort_values(ascending=False).head(10)
    fig = px.bar(top_rev, x=top_rev.values, y=top_rev.index,
                 orientation='h', height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🚚 Delivery vs Review")
    review_delivery = df_filtered.groupby('is_late')['review_score'].mean().reset_index()
    fig = px.bar(review_delivery, x='is_late', y='review_score',
                 color='is_late', height=350)
    st.plotly_chart(fig, use_container_width=True)

# DISTRIBUSI DELAY 
st.subheader("📦 Distribusi Keterlambatan Pengiriman")

lower = df_filtered['delivery_delay'].quantile(0.01)
upper = df_filtered['delivery_delay'].quantile(0.99)

filtered_delay = df_filtered[
    (df_filtered['delivery_delay'] >= lower) &
    (df_filtered['delivery_delay'] <= upper)
]

fig = px.histogram(
    filtered_delay,
    x='delivery_delay',
    nbins=50,
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.caption("Distribusi difilter (1%–99%) agar outlier ekstrem tidak merusak pola utama.")


# RFM FIX (ANTI ERROR)

st.subheader("👤 RFM Segmentation")

snapshot = df_filtered['order_purchase_timestamp'].max()

rfm = df_filtered.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot - x.max()).days,
    'order_id': 'count',
    'revenue': 'sum'
}).reset_index()

rfm.columns = ['customer_id','recency','frequency','monetary']

def safe_qcut(series):
    try:
        return pd.qcut(series, 4, labels=False, duplicates='drop') + 1
    except:
        return pd.cut(series, bins=4, labels=False) + 1

rfm['R'] = safe_qcut(rfm['recency'])
rfm['F'] = safe_qcut(rfm['frequency'])
rfm['M'] = safe_qcut(rfm['monetary'])

rfm['score'] = rfm[['R','F','M']].sum(axis=1)

rfm['segment'] = pd.qcut(
    rfm['score'],
    4,
    labels=["Low", "Mid", "High", "Top"],
    duplicates='drop'
)

# PIE
st.subheader("👥 Distribusi Segment RFM")
seg = rfm['segment'].value_counts().reset_index()
seg.columns = ['segment','count']

fig = px.pie(seg, names='segment', values='count', height=300)
st.plotly_chart(fig, use_container_width=True)

# SCATTER FULL
st.subheader("📍 Distribusi Customer (RFM)")

fig = px.scatter(
    rfm,
    x='recency',
    y='monetary',
    color='segment',
    size='frequency',
    size_max=15,
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.caption("Semakin kanan = customer lama tidak beli, semakin atas = revenue tinggi.")

# SELLER
st.subheader("🏪 Performa Seller (Keterlambatan & Volume Order)")

seller_perf = df_filtered.groupby('seller_id').agg({
    'order_id': 'count',
    'is_late': 'mean'
}).reset_index()

seller_perf.columns = ['seller_id', 'total_orders', 'late_rate']

seller_perf = seller_perf[seller_perf['total_orders'] > 20]
seller_perf = seller_perf.sort_values(by='late_rate', ascending=False).head(10)

fig = px.bar(
    seller_perf,
    x='seller_id',
    y='late_rate',
    color='total_orders',
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# DATA
st.subheader("📄 Data Preview")
st.dataframe(df_filtered.head(100))