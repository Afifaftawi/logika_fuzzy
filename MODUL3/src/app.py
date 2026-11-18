
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import base64
from pathlib import Path

from fuzzy_engine import (
    hitung_fuzzy,
    fuzzifikasi_rapor,
    fuzzifikasi_tes
)
st.set_page_config(
    page_title="SIPENA",
    page_icon="",
    layout="wide"
)

gambar_path = Path(__file__).parent / "background_app.jpeg"

gambar_base64 = ""

if gambar_path.exists():
    with open(gambar_path, "rb") as file:
        gambar_base64 = base64.b64encode(file.read()).decode()

st.markdown(f"""
<style>

/* Background utama */
.stApp {{
    background-image:
        linear-gradient(
            rgba(240, 253, 250, 0.62),
            rgba(240, 253, 250, 0.72)
        ),
        url("data:image/jpeg;base64,{gambar_base64}");

    background-size: cover;
    background-position: 30% 30% !important;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Area utama */
.block-container {{
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}

/* Header Streamlit */
[data-testid="stHeader"] {{
    background: transparent;
}}

/* Judul */
h1 {{
    color: #064E4D !important;
    font-weight: 750 !important;
    letter-spacing: -1px;
}}

h2, h3 {{
    color: #0F766E !important;
    font-weight: 650 !important;
}}

p {{
    color: #475569;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: #064E4D;
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

/* Input angka */
[data-testid="stSidebar"] input {{
    background: white !important;
    color: #064E4D !important;
}}

[data-testid="stSidebar"] [data-baseweb="input"] {{
    background: white;
    border-radius: 8px;
}}

/* Tombol minus dan plus */
[data-testid="stNumberInput"] button {{
    background-color: #0F8B8D !important;
    color: #FFFFFF !important;
    border: 1px solid #0F8B8D !important;
    opacity: 1 !important;
}}

[data-testid="stNumberInput"] button:hover {{
    background-color: #064E4D !important;
    color: #FFFFFF !important;
}}

[data-testid="stNumberInput"] button svg {{
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}}

/* Tombol cek nilai */
.stFormSubmitButton button {{
    background: #0F8B8D !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    padding: 10px !important;
}}

.stFormSubmitButton button:hover {{
    background: #064E4D !important;
    color: white !important;
}}

/* Kartu metrik */
[data-testid="stMetric"] {{
    background: #FFFFFF;
    border: 1px solid #CBF3F0;
    border-left: 4px solid #0F8B8D;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(6,78,77,0.07);
}}

[data-testid="stMetricLabel"] {{
    color: #64748b !important;
}}

[data-testid="stMetricValue"] {{
    color: #064E4D !important;
    font-weight: 750 !important;
}}

/* Status diterima */
.status-diterima {{
    background: #CBF3F0;
    border: 1px solid #5EEAD4;
    border-left: 5px solid #0F8B8D;
    border-radius: 12px;
    padding: 22px;
    text-align: center;
    color: #064E4D;
    font-size: 20px;
    font-weight: bold;
}}

/* Status tidak diterima */
.status-ditolak {{
    background: #FEE2E2;
    border: 1px solid #FCA5A5;
    border-left: 5px solid #DC2626;
    border-radius: 12px;
    padding: 22px;
    text-align: center;
    color: #991B1B;
    font-size: 20px;
    font-weight: bold;
}}

/* Progress bar tunggal */
.progress-track {{
    width: 100%;
    height: 14px;
    background: #E2E8F0;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 10px;
}}

.progress-fill {{
    height: 100%;
    background: linear-gradient(
        90deg,
        #DC2626 0%,
        #FACC15 50%,
        #16A34A 100%
    );
    border-radius: 20px;
    transition: width 0.4s ease;
}}

/* Tabel */
[data-testid="stDataFrame"] {{
    background: white;
    border: 1px solid #CBF3F0;
    border-radius: 12px;
}}

/* Informasi sistem */
.info {{
    background: #FFFFFF;
    border-left: 5px solid #0F8B8D;
    padding: 20px;
    border-radius: 10px;
    color: #064E4D;
    box-shadow: 0 3px 12px rgba(6,78,77,0.07);
    line-height: 1.8;
}}

/* Garis pemisah */
hr {{
    border-color: #B2E8E3;
}}

</style>
""", unsafe_allow_html=True)

st.caption("UNIVERSITAS ISLAM NEGERI MATARAM")

st.title("SIPENA")

st.markdown("""
Sistem penentuan nilai akhir seleksi penerimaan calon mahasiswa baru .
""")

st.divider()

if "nilai_rapor" not in st.session_state:
    st.session_state.nilai_rapor = 75

if "nilai_tes" not in st.session_state:
    st.session_state.nilai_tes = 75

if "sudah_dicek" not in st.session_state:
    st.session_state.sudah_dicek = True


st.sidebar.title("INPUT NILAI CALON MAHASISWA BARU")

st.sidebar.write(
    "Masukkan nilai rapor dan nilai tes tulis calon mahasiswa."
)

with st.sidebar.form("form_nilai"):

    input_rapor = st.number_input(
        "Nilai Rapor",
        min_value=0,
        max_value=100,
        value=st.session_state.nilai_rapor,
        step=1
    )

    input_tes = st.number_input(
        "Nilai Tes Tulis",
        min_value=0,
        max_value=100,
        value=st.session_state.nilai_tes,
        step=1
    )

    cek_nilai = st.form_submit_button(
        "CEK NILAI",
        use_container_width=True
    )


if cek_nilai:

    st.session_state.nilai_rapor = input_rapor
    st.session_state.nilai_tes = input_tes
    st.session_state.sudah_dicek = True


nilai_rapor = st.session_state.nilai_rapor
nilai_tes = st.session_state.nilai_tes

st.sidebar.divider()

st.sidebar.caption("Rentang nilai: 0–100")

hasil = hitung_fuzzy(nilai_rapor, nilai_tes)

nilai_akhir = hasil["nilai_akhir"]
keputusan = hasil["keputusan"]
detail_aturan = hasil["detail_aturan"]

hasil_rapor = fuzzifikasi_rapor(nilai_rapor)
hasil_tes = fuzzifikasi_tes(nilai_tes)


# Menentukan kategori linguistik input
kategori_rapor = max(
    hasil_rapor,
    key=hasil_rapor.get
)

kategori_tes = max(
    hasil_tes,
    key=hasil_tes.get
)


# Menentukan kategori linguistik output
# Berdasarkan titik tengah konstanta Sugeno

if nilai_akhir < 35:
    kategori_akhir = "Rendah"

elif nilai_akhir < 65:
    kategori_akhir = "Sedang"

else:
    kategori_akhir = "Tinggi"

st.subheader("Hasil Seleksi")

kolom1, kolom2, kolom3 = st.columns(3)

with kolom1:

    st.metric(
        label="Nilai Rapor",
        value=f"{nilai_rapor}"
    )

with kolom2:

    st.metric(
        label="Nilai Tes Tulis",
        value=f"{nilai_tes}"
    )

with kolom3:

    st.metric(
        label="Nilai Akhir Seleksi",
        value=f"{nilai_akhir:.2f}"
    )

if keputusan == "DITERIMA":

    st.markdown(
        """
        <div class="status-diterima">
            ✓ CALON MAHASISWA DITERIMA
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="status-ditolak">
            CALON MAHASISWA TIDAK DITERIMA
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

st.markdown("**Persentase Nilai Akhir Seleksi**")

persentase = min(
    max(float(nilai_akhir), 0),
    100
)

st.markdown(
    f"""
    <div class="progress-track">
        <div class="progress-fill"
             style="width: {persentase}%;">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Nilai akhir: {nilai_akhir:.2f} dari 100"
)

st.markdown("### Kategori Linguistik Nilai Akhir")

if kategori_akhir == "Rendah":

    st.error(
        f"Kategori nilai akhir: {kategori_akhir}"
    )

elif kategori_akhir == "Sedang":

    st.warning(
        f"Kategori nilai akhir: {kategori_akhir}"
    )

else:

    st.success(
        f"Kategori nilai akhir: {kategori_akhir}"
    )


st.divider()

st.subheader("Hasil Fuzzifikasi dan Kategori Linguistik")

kolom1, kolom2 = st.columns(2)

with kolom1:

    st.markdown("**Fuzzifikasi Nilai Rapor**")

    st.metric(
        label="Kategori Linguistik",
        value=kategori_rapor
    )

    data_rapor = pd.DataFrame(
        list(hasil_rapor.items()),
        columns=["Kategori", "Derajat Keanggotaan"]
    )

    data_rapor["Derajat Keanggotaan"] = (
        data_rapor["Derajat Keanggotaan"].round(3)
    )

    st.dataframe(
        data_rapor,
        use_container_width=True,
        hide_index=True
    )


with kolom2:

    st.markdown("**Fuzzifikasi Nilai Tes Tulis**")

    st.metric(
        label="Kategori Linguistik",
        value=kategori_tes
    )

    data_tes = pd.DataFrame(
        list(hasil_tes.items()),
        columns=["Kategori", "Derajat Keanggotaan"]
    )

    data_tes["Derajat Keanggotaan"] = (
        data_tes["Derajat Keanggotaan"].round(3)
    )

    st.dataframe(
        data_tes,
        use_container_width=True,
        hide_index=True
    )

st.divider()

st.subheader("Visualisasi Aktivasi Aturan Fuzzy")

st.write("""
Grafik berikut menunjukkan nilai firing strength
dari setiap aturan fuzzy yang digunakan dalam proses inferensi.
""")

nama_aturan = []
nilai_alpha = []

for aturan in detail_aturan:

    nama_aturan.append(aturan["aturan"])
    nilai_alpha.append(aturan["alpha"])


fig, ax = plt.subplots(figsize=(10, 5))

ax.barh(
    nama_aturan,
    nilai_alpha,
    color="#0F8B8D",
    edgecolor="#064E4D"
)

ax.set_xlabel("Firing Strength")
ax.set_ylabel("Aturan Fuzzy")
ax.set_title("Aktivasi 9 Aturan Fuzzy Sugeno")

ax.set_xlim(0, 1)
ax.set_facecolor("#FFFFFF")
fig.patch.set_facecolor("#FFFFFF")

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.3
)

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)

st.subheader("Detail Perhitungan Aturan")

data_aturan = []

for aturan in detail_aturan:

    data_aturan.append({
        "Aturan": aturan["aturan"],
        "Firing Strength": round(
            aturan["alpha"], 4
        ),
        "Konstanta Sugeno": aturan["konstanta"]
    })

df_aturan = pd.DataFrame(data_aturan)

st.dataframe(
    df_aturan,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Informasi Sistem")

st.markdown("""
<div class="info">

<b>Metode Inferensi:</b> Sugeno Orde 0

<br>

<b>Operator Fuzzy:</b> AND (Minimum)

<br>

<b>Defuzzifikasi:</b> Weighted Average

<br>

<b>Konstanta Output:</b> 20, 50, dan 80

<br>

<b>Ambang Batas Kelulusan:</b> 60

<br>

<b>Rentang Nilai:</b> 0–100

</div>
""", unsafe_allow_html=True)

st.write("")

st.divider()

st.caption(
    "Sistem Pendukung Keputusan Seleksi Penerimaan Mahasiswa Baru"
)

st.caption(
    "Sistem ini merupakan simulasi saja, yang Dibangun menggunakan Python, Streamlit, dan Logika Fuzzy Sugeno Orde 0. untuk keperluan tugas matakuliah Logika Fuzzy Mahasiswa Teknologi Informasi UIN Mataram"
)
