import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Judul Aplikasi Web
st.title("Aplikasi Simulasi Monte Carlo: Risiko Keterlambatan Proyek Konstruksi")
st.write("Aplikasi ini dibuat untuk memenuhi Tugas Akhir (TA-03) Pemodelan dan Simulasi.")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv('construction_project_dataset.csv', sep=';', low_memory=False)
    df['time_deviation'] = df['time_deviation'].astype(str).str.replace(',', '.').astype(float)
    return df.dropna(subset=['time_deviation'])

df = load_data()
time_dev = df['time_deviation']
mu = np.mean(time_dev)
sigma = np.std(time_dev)

# --- BAGIAN INPUT INTERAKTIF (Bisa diubah sendiri oleh pengguna) ---
st.sidebar.header("⚙️ Pengaturan Parameter Simulasi")

# 1. Input untuk jumlah skenario (slider)
num_points = st.sidebar.slider("Jumlah Skenario (Iterasi)", min_value=1000, max_value=20000, value=5000, step=1000)

# 2. Input untuk batas toleransi keterlambatan (angka / number_input)
threshold_limit = st.sidebar.number_input("Batas Toleransi Keterlambatan (Hari)", min_value=10.0, max_value=200.0, value=70.0, step=1.0)

# 3. Input untuk durasi baseline proyek (angka / number_input)
base_duration = st.sidebar.number_input("Durasi Baseline Proyek (Hari)", min_value=10, max_value=150, value=60, step=1)
# -----------------------------------------------------------------

# Proses Simulasi Monte Carlo berdasarkan nilai input
np.random.seed(301240013) # NIM Anda
simulated_time_dev = np.random.normal(mu, sigma, num_points)
simulated_total_duration = base_duration + simulated_time_dev

exceeded_limit = simulated_total_duration > threshold_limit
jumlah_terlambat = np.sum(exceeded_limit)
probability = jumlah_terlambat / num_points

# Hasil Analisis
st.subheader("📊 Hasil Analisis Risiko")

st.markdown(f"""
---
* **Total Skenario Simulasi:** `{num_points}`
* **Durasi Baseline Proyek:** `{base_duration} Hari`
* **Batas Toleransi:** `{threshold_limit} Hari`
* **Probabilitas Keterlambatan Proyek:** `{(jumlah_terlambat / num_points) * 100:.2f}%`
---
""")

st.write(f"Dari **{num_points}** skenario simulasi, terdapat **{jumlah_terlambat}** skenario yang durasi totalnya melebihi batas **{threshold_limit} hari**.")

# Visualisasi Grafik
st.subheader("📈 Grafik Distribusi Skenario Proyek")
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(simulated_total_duration, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
ax.axvline(threshold_limit, color='red', linestyle='dashed', linewidth=2, label=f'Batas Toleransi ({threshold_limit} Hari)')
ax.set_title("Simulasi Monte Carlo: Risiko Keterlambatan Proyek")
ax.set_xlabel("Total Durasi Proyek (Hari)")
ax.set_ylabel("Frekuensi Skenario")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)