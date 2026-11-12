# Proyek Analisis Data - Bike Sharing

## Deskripsi
Proyek ini menganalisis data penyewaan sepeda menggunakan Bike Sharing Dataset periode 2011–2012.

Analisis mencakup Data Wrangling, Exploratory Data Analysis (EDA), visualisasi data, dan analisis lanjutan. Hasil analisis disajikan melalui dashboard interaktif menggunakan Streamlit.

## Business Questions
1. Bagaimana pola jumlah penyewaan sepeda berdasarkan jam dalam sehari selama periode 2011–2012?
2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca selama periode 2011–2012?

## Dataset
- day.csv: Data penyewaan sepeda harian.
- hour.csv: Data penyewaan sepeda per jam.
- day_clean.csv: Data harian setelah proses cleaning.
- hour_clean.csv: Data per jam setelah proses cleaning.

## Tools
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Google Colab

## Struktur Proyek
- dashboard/: Kode dashboard Streamlit.
- data/: Dataset asli dan hasil cleaning.
- Proyek_Analisis_Data_Bike_Sharing.ipynb: Notebook analisis.
- requirements.txt: Daftar library.
- url.txt: Tautan dashboard online.

## Cara Menjalankan Dashboard

Instal library:

pip install -r requirements.txt

Jalankan dashboard:

streamlit run dashboard/dashboard.py

Dashboard lokal dapat diakses melalui:

http://localhost:8501