import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from src.fuzzy_engine import hitung_fuzzy

folder = Path(__file__).parent
file_csv = folder / "data" / "test_cases.csv"
df = pd.read_csv(file_csv)

print("==========================================")
print(" SISTEM FUZZY SIPENA ")
print("==========================================")

print("\nDATASET AWAL")
print(df)

print("\nJumlah data awal:", len(df))


kolom_wajib = [
    "id",
    "nilai_rapor",
    "nilai_tes_tulis",
    "nilai_target"
]

if not all(kolom in df.columns for kolom in kolom_wajib):
    print("\nKolom dataset tidak lengkap.")
    exit()

kolom_nilai = [
    "nilai_rapor",
    "nilai_tes_tulis",
    "nilai_target"
]

for kolom in kolom_nilai:
    df[kolom] = pd.to_numeric(df[kolom], errors="coerce")

df = df.dropna(subset=kolom_wajib)

for kolom in kolom_nilai:
    df = df[(df[kolom] >= 0) & (df[kolom] <= 100)]

print("\nDATA SETELAH PREPROCESSING")
print(df)

print("\nJumlah data setelah preprocessing:", len(df))

hasil_prediksi = []

for index, baris in df.iterrows():

    hasil = hitung_fuzzy(
        baris["nilai_rapor"],
        baris["nilai_tes_tulis"]
    )

    hasil_prediksi.append(hasil["nilai_akhir"])

df["nilai_prediksi"] = hasil_prediksi


df["error"] = df["nilai_target"] - df["nilai_prediksi"]
df["absolute_error"] = abs(df["error"])

mae = np.mean(df["absolute_error"])
rmse = np.sqrt(np.mean(df["error"] ** 2))


print("\n==========================================")
print(" HASIL PENGUJIAN BATCH")
print("==========================================")

print(
    df[
        [
            "id",
            "nilai_rapor",
            "nilai_tes_tulis",
            "nilai_target",
            "nilai_prediksi",
            "error"
        ]
    ].round(2).to_string(index=False)
)

print("\n==========================================")
print(" HASIL EVALUASI ERROR")
print("==========================================")

print(f"Jumlah data : {len(df)}")
print(f"MAE         : {mae:.2f}")
print(f"RMSE        : {rmse:.2f}")


data_error = df.sort_values(
    by="absolute_error",
    ascending=False
).head(2)

print("\n==========================================")
print(" DUA DATA DENGAN ERROR TERBESAR")
print("==========================================")

print(
    data_error[
        [
            "id",
            "nilai_rapor",
            "nilai_tes_tulis",
            "nilai_target",
            "nilai_prediksi",
            "absolute_error"
        ]
    ].round(2).to_string(index=False)
)

plt.figure(figsize=(10, 5))

plt.plot(
    df["id"],
    df["nilai_target"],
    marker="o",
    label="Nilai Target"
)

plt.plot(
    df["id"],
    df["nilai_prediksi"],
    marker="s",
    label="Prediksi Fuzzy"
)

plt.title("Perbandingan Nilai Target dan Prediksi Fuzzy")
plt.xlabel("ID Pelamar")
plt.ylabel("Nilai Akhir")
plt.xticks(df["id"])
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(folder / "hasil_evaluasi.png")

plt.show()

print("\nGrafik berhasil disimpan sebagai hasil_evaluasi.png")
print("\nPengujian batch selesai.")
