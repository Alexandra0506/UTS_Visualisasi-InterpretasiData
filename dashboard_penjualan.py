# ==============================================================
# DASHBOARD PENJUALAN E-COMMERCE
# Analisis Promosi & Perilaku Pelanggan (Kasus 1)
# ==============================================================
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# --------------------------------------------------------------
# KONFIGURASI HALAMAN
# --------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Penjualan & Promosi",
    layout="wide",
    page_icon="📊"
)
sns.set_style("whitegrid")

# --------------------------------------------------------------
# FUNGSI MEMUAT DATA
# --------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("finalProj_df.csv", parse_dates=["order_date", "registered_date"])
    df["order_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df

df = load_data()

# --------------------------------------------------------------
# SIDEBAR FILTER
# --------------------------------------------------------------
st.sidebar.header("🔎 Filter Data")

start_date = st.sidebar.date_input("Tanggal Awal", df["order_date"].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df["order_date"].max().date())
kategori = st.sidebar.multiselect("Pilih Kategori Produk", df["category"].unique())
payment = st.sidebar.multiselect("Pilih Metode Pembayaran", df["payment_method"].unique())

# Terapkan filter
mask = (df["order_date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
if kategori:
    mask &= df["category"].isin(kategori)
if payment:
    mask &= df["payment_method"].isin(payment)

df_filtered = df[mask]

# --------------------------------------------------------------
# BAGIAN KPI (Key Performance Indicator)
# --------------------------------------------------------------
st.title("📊 Dashboard Analisis Penjualan & Promosi")
st.markdown("Dashboard ini digunakan untuk menganalisis efektivitas diskon, tren penjualan, kategori produk, dan preferensi metode pembayaran.")

col1, col2, col3, col4 = st.columns(4)

total_revenue = df_filtered["after_discount"].sum()
total_discount = df_filtered["discount_amount"].sum()
avg_order_value = df_filtered["after_discount"].mean()
active_customers = df_filtered["customer_id"].nunique()

col1.metric("💰 Total Penjualan", f"{total_revenue:,.0f}")
col2.metric("🏷️ Total Diskon Diberikan", f"{total_discount:,.0f}")
col3.metric("📦 Rata-rata Order Value", f"{avg_order_value:,.0f}")
col4.metric("👥 Pelanggan Aktif", active_customers)

st.markdown("---")

# --------------------------------------------------------------
# GRAFIK 1: TREN PENJUALAN PER BULAN
# --------------------------------------------------------------
st.subheader("📈 Tren Penjualan per Bulan")

df_month = (
    df_filtered.groupby("order_month")["after_discount"]
    .sum()
    .reset_index()
    .sort_values("order_month")
)

fig1 = px.line(
    df_month,
    x="order_month",
    y="after_discount",
    markers=True,
    title="Tren Penjualan Setelah Diskon",
    color_discrete_sequence=["#2E86C1"]
)
fig1.update_layout(xaxis_title="Bulan", yaxis_title="Total Penjualan")
st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------------------
# GRAFIK 2: DAMPAK DISKON TERHADAP PENJUALAN
# --------------------------------------------------------------
st.subheader("💡 Dampak Diskon terhadap Volume Penjualan")

df_discount = (
    df_filtered.groupby("order_month")
    .agg({"discount_amount": "sum", "after_discount": "sum"})
    .reset_index()
)

fig2 = px.bar(
    df_discount,
    x="order_month",
    y="discount_amount",
    labels={"discount_amount": "Total Diskon"},
    title="Total Diskon (Bar) dan Penjualan (Line)",
    color_discrete_sequence=["#F39C12"]
)
fig2.add_scatter(
    x=df_discount["order_month"],
    y=df_discount["after_discount"],
    mode="lines+markers",
    name="Penjualan",
    line=dict(color="#2980B9", width=3)
)
fig2.update_layout(xaxis_title="Bulan", yaxis_title="Nilai Diskon")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------------------
# GRAFIK 3: DISTRIBUSI PENJUALAN BERDASARKAN KATEGORI
# --------------------------------------------------------------
st.subheader("🛍️ Distribusi Penjualan Berdasarkan Kategori Produk")

df_cat = (
    df_filtered.groupby("category")["after_discount"]
    .sum()
    .reset_index()
    .sort_values("after_discount", ascending=False)
)

fig3 = px.bar(
    df_cat,
    x="after_discount",
    y="category",
    orientation="h",
    title="Kategori Produk dengan Penjualan Tertinggi",
    color="after_discount",
    color_continuous_scale="Blues"
)
fig3.update_layout(xaxis_title="Total Penjualan", yaxis_title="Kategori")
st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------------------
# GRAFIK 4: METODE PEMBAYARAN
# --------------------------------------------------------------
st.subheader("💳 Proporsi Penjualan Berdasarkan Metode Pembayaran")

df_payment = (
    df_filtered.groupby("payment_method")["after_discount"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    df_payment,
    names="payment_method",
    values="after_discount",
    title="Metode Pembayaran yang Paling Banyak Digunakan",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------------------------
# GRAFIK 5: PELANGGAN AKTIF PER BULAN
# --------------------------------------------------------------
st.subheader("👥 Jumlah Pelanggan Aktif per Bulan")

df_customers = (
    df_filtered.groupby("order_month")["customer_id"]
    .nunique()
    .reset_index()
)

fig5 = px.area(
    df_customers,
    x="order_month",
    y="customer_id",
    title="Jumlah Pelanggan Unik Aktif per Bulan",
    color_discrete_sequence=["#27AE60"]
)
fig5.update_layout(xaxis_title="Bulan", yaxis_title="Jumlah Pelanggan Aktif")
st.plotly_chart(fig5, use_container_width=True)

# --------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 Dashboard Analitik Promosi — dikembangkan untuk analisis efektivitas promosi dan perilaku pelanggan e-commerce.")

