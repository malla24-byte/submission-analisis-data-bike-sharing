
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================
# 1. KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# =====================================
# 2. MEMUAT DATASET
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data
def load_data():
    day = pd.read_csv(DATA_DIR / "day_clean.csv")
    hour = pd.read_csv(DATA_DIR / "hour_clean.csv")

    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])

    return day, hour

try:
    day_df, hour_df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset tidak ditemukan. Periksa folder data "
        "dan pastikan file CSV tersedia."
    )
    st.stop()

# =====================================
# 3. LABEL DATA
# =====================================

year_labels = {0: "2011", 1: "2012"}

season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_labels = {
    1: "Clear / Partly Cloudy",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow"
}

for df in [day_df, hour_df]:
    df["year_label"] = df["yr"].map(year_labels)
    df["season_label"] = df["season"].map(season_labels)
    df["weather_label"] = df["weathersit"].map(weather_labels)

# =====================================
# 4. JUDUL DASHBOARD
# =====================================

st.title("🚲 Bike Sharing Dashboard")

st.write(
    """
    Dashboard ini menyajikan analisis data penyewaan sepeda
    berdasarkan jam, kondisi cuaca, dan musim selama tahun 2011–2012.
    """
)

st.divider()

# =====================================
# 5. FILTER DATA
# =====================================

st.sidebar.header("Filter Data")

year_options = ["2011", "2012"]
season_options = ["Spring", "Summer", "Fall", "Winter"]

weather_options = sorted(
    day_df["weather_label"].dropna().unique().tolist()
)

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=year_options,
    default=year_options
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=season_options,
    default=season_options
)

selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=weather_options,
    default=weather_options
)

# =====================================
# 6. FILTER DATASET
# =====================================

def apply_filter(df):
    return df[
        df["year_label"].isin(selected_year)
        & df["season_label"].isin(selected_season)
        & df["weather_label"].isin(selected_weather)
    ]

filtered_day = apply_filter(day_df)
filtered_hour = apply_filter(hour_df)

if filtered_day.empty or filtered_hour.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter tersebut. "
        "Silakan ubah pilihan filter."
    )
    st.stop()

# =====================================
# 7. INFORMASI RINGKASAN / KPI
# =====================================

total_rentals = filtered_day["cnt"].sum()
average_rentals = filtered_day["cnt"].mean()
total_days = filtered_day["dteday"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Penyewaan",
    f"{total_rentals:,.0f}"
)

col2.metric(
    "Rata-rata Penyewaan Harian",
    f"{average_rentals:,.2f}"
)

col3.metric(
    "Jumlah Hari",
    f"{total_days:,}"
)

st.divider()

# =====================================
# 8. GRAFIK BERDASARKAN JAM
# =====================================

st.subheader("Pola Penyewaan Sepeda Berdasarkan Jam")

hourly_rentals = (
    filtered_hour.groupby("hr")["cnt"]
    .mean()
    .reset_index()
)

fig_hour = px.line(
    hourly_rentals,
    x="hr",
    y="cnt",
    markers=True,
    title="Rata-rata Penyewaan Sepeda Berdasarkan Jam",
    labels={
        "hr": "Jam",
        "cnt": "Rata-rata Jumlah Penyewaan"
    }
)

fig_hour.update_layout(
    xaxis=dict(tickmode="linear", dtick=1)
)

st.plotly_chart(fig_hour, width="stretch")

# =====================================
# 9. GRAFIK BERDASARKAN CUACA
# =====================================

st.subheader("Penyewaan Sepeda Berdasarkan Kondisi Cuaca")

weather_rentals = (
    filtered_day.groupby("weather_label")["cnt"]
    .mean()
    .reset_index()
    .sort_values("cnt", ascending=False)
)

fig_weather = px.bar(
    weather_rentals,
    x="weather_label",
    y="cnt",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Kondisi Cuaca",
    labels={
        "weather_label": "Kondisi Cuaca",
        "cnt": "Rata-rata Jumlah Penyewaan"
    }
)

st.plotly_chart(fig_weather, width="stretch")

# =====================================
# 10. GRAFIK BERDASARKAN MUSIM
# =====================================

st.subheader("Penyewaan Sepeda Berdasarkan Musim")

season_rentals = (
    filtered_day.groupby("season_label")["cnt"]
    .mean()
    .reindex(season_options)
    .dropna()
    .reset_index()
)

fig_season = px.bar(
    season_rentals,
    x="season_label",
    y="cnt",
    text_auto=".2f",
    title="Rata-rata Penyewaan Berdasarkan Musim",
    labels={
        "season_label": "Musim",
        "cnt": "Rata-rata Jumlah Penyewaan"
    }
)

st.plotly_chart(fig_season, width="stretch")

# =====================================
# 11. TABEL DATA
# =====================================

st.subheader("Data Penyewaan Sepeda")

st.dataframe(
    filtered_day[
        [
            "dteday",
            "year_label",
            "season_label",
            "weather_label",
            "casual",
            "registered",
            "cnt"
        ]
    ].sort_values("dteday"),
    width="stretch"
)
# =====================================
# 12. FOOTER
# =====================================

st.divider()

st.caption(
    "Bike Sharing Data Analysis | Dataset periode 2011–2012"
)
