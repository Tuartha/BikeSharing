import os
os.system("pip install --no-cache-dir matplotlib seaborn")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    return pd.read_csv(file_path, parse_dates=['dteday'])

df = load_data()
df["dteday"] = df["dteday"].dt.date

# Sidebar
st.sidebar.title("Bikers Santuy 🚲")
season_filter = st.sidebar.multiselect("Pilih Musim:", df["season_day"].unique())
weather_filter = st.sidebar.multiselect("Pilih Cuaca:", df["weathersit_hour"].unique())
if not season_filter and not weather_filter:
    df_filtered = df 
else:
    df_filtered = df[
        (df["season_day"].isin(season_filter) if season_filter else True) & 
        (df["weathersit_hour"].isin(weather_filter) if weather_filter else True)
    ]

# Jika hasil filtering kosong, tampilkan pesan
if df_filtered.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
else:
    #Analisis Peningkatan Penyewaan Sepeda
    st.title("Analisis Peningkatan Penyewaan Sepeda")
    year_compare = df_filtered.groupby(['yr_day'])['cnt_day'].mean()
    max_value = year_compare.max()
    colors = ["#D3D3D3" if value < max_value else "#72BCD4" for value in year_compare.values]
    st.subheader("Perbandingan Rata-rata Jumlah Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=year_compare.index, y=year_compare.values, ax=ax, palette=colors)
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(fig)

    #Analisis Pengaruh Pergantian Musim
    st.title("Analisis Pengaruh Pergantian Musim")
    season_analysis = df_filtered.groupby(['season_day'])['cnt_day'].mean().reset_index()
    season_analysis = season_analysis.sort_values(by="cnt_day", ascending=False)
    max_value = season_analysis.cnt_day.max()
    colors = ["#D3D3D3" if value < max_value else "#72BCD4" for value in season_analysis['cnt_day'].tolist()]
    st.subheader("Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="season_day", y="cnt_day", data=season_analysis, ax=ax, palette=colors)
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(fig)

    #Analisis Pengaruh Pergantian Cuaca
    st.title("Analisis Pengaruh Pergantian Cuaca")
    weather_analysis = df_filtered.groupby(['weathersit_hour'])['cnt_hour'].mean().reset_index()
    max_value = weather_analysis.cnt_hour.max()
    colors = ["#D3D3D3" if value < max_value else "#72BCD4" for value in weather_analysis['cnt_hour'].tolist()]
    st.subheader("Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x="weathersit_hour", y="cnt_hour", data=weather_analysis.sort_values(by="cnt_hour", ascending=False), ax=ax, palette=colors)
    ax.set_xlabel('Cuaca')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    st.pyplot(fig)

    #Analisis Pola Penyewaan Sepeda Berdasarkan Waktu
    st.title("Analisis Pola Penyewaan Sepeda Berdasarkan Waktu")
    pola_pinjam = df_filtered.groupby(["weekday_hour", "hr"])["cnt_hour"].mean().reset_index()
    hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    pola_pinjam["weekday_hour"] = pd.Categorical(pola_pinjam["weekday_hour"], categories=hari, ordered=True)
    pola_pinjam = pola_pinjam.sort_values(by="weekday_hour")
        
    st.subheader("Rata-rata Jumlah Peminjaman Sepeda Berdasarkan Waktu")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="weekday_hour", y="cnt_hour", hue="hr", data=pola_pinjam, ax=ax)
    ax.set_xlabel('Hari')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax.legend(title='Waktu')
    st.pyplot(fig)

# **Jalankan aplikasi**
if __name__ == "__main__":
    st.write("Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")
