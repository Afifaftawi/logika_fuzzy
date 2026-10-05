import mysql.connector

# Koneksi khusus MAMP di macOS
db = mysql.connector.connect(
    host="127.0.0.1",
    port=8889,                       # Port default MAMP adalah 8889
    user="root",
    password="root",                 # Password default MAMP adalah "root"
    database="praktikum3_fuzzy",
    unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock"
)

print("Koneksi database berhasil!")
# ==========================================================
# 2. DEFINISI FUNGSI KEANGGOTAAN TRAPESIUM
# ==========================================================
# Kategori Balita (0-6 tahun)
def trapesium_up_balita(x):
    return x

def trapesium_down_balita(x):
    return (-x + 6) / 2

# Kategori Anak-anak (5-12 tahun)
def trapesium_up_anak(x):
    return (x - 5) / 2

def trapesium_down_anak(x):
    return (-x + 12) / 2

# Kategori Remaja (11-20 tahun)
def trapesium_up_remaja(x):
    return (x - 11) / 2

def trapesium_down_remaja(x):
    return (-x + 20) / 2

# Kategori Dewasa (18-60 tahun)
def trapesium_up_dewasa(x):
    return (x - 18) / 7

def trapesium_down_dewasa(x):
    return (-x + 60) / 10

# Kategori Lansia (55-80 tahun)
def trapesium_up_lansia(x):
    return (x - 55) / 7

def trapesium_down_lansia(x):
    return (-x + 80) / 5

# ==========================================================
# 3. MAPPING STRING DATABASE KE FUNGSI PYTHON
# ==========================================================
fungsi_dict = {
    "trapesium_up_balita": trapesium_up_balita,
    "trapesium_down_balita": trapesium_down_balita,
    "trapesium_up_anak": trapesium_up_anak,
    "trapesium_down_anak": trapesium_down_anak,
    "trapesium_up_remaja": trapesium_up_remaja,
    "trapesium_down_remaja": trapesium_down_remaja,
    "trapesium_up_dewasa": trapesium_up_dewasa,
    "trapesium_down_dewasa": trapesium_down_dewasa,
    "trapesium_up_lansia": trapesium_up_lansia,
    "trapesium_down_lansia": trapesium_down_lansia,
}

# ==========================================================
# 4. FUNGSI FUZZIFIKASI DINAMIS
# ==========================================================
def fuzzifikasi_usia(tabel_nama, x):
    cursor = db.cursor()
    query = f"""
        SELECT b_bawah, b_atas, fungsi 
        FROM {tabel_nama} 
        WHERE %s >= b_bawah AND %s <= b_atas
    """
    cursor.execute(query, (x, x))
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return 0.0

    b_bawah, b_atas, nama_fungsi = data

    if nama_fungsi == "0":
        return 0.0
    if nama_fungsi == "1":
        return 1.0
    if nama_fungsi in fungsi_dict:
        fungsi_y = fungsi_dict[nama_fungsi]
        nilai = fungsi_y(x)
        return round(nilai, 2)

    raise ValueError(f"Fungsi '{nama_fungsi}' belum didefinisikan di Python.")

# ==========================================================
# 5. PENGUJIANKOMPREHENSIF (12 DATA UJI)
# ==========================================================
data_uji = [
    ("Balita", "usia_balita", 0.5, "0–1"),
    ("Balita", "usia_balita", 5.0, "4–6"),
    ("Anak-anak", "usia_anak", 6.0, "5–7"),
    ("Anak-anak", "usia_anak", 11.0, "10–12"),
    ("Remaja", "usia_remaja", 12.0, "11–13"),
    ("Remaja", "usia_remaja", 19.0, "18–20"),
    ("Dewasa", "usia_dewasa", 21.5, "18–25"),
    ("Dewasa", "usia_dewasa", 55.0, "50–60"),
    ("Lansia", "usia_lansia", 58.5, "55–62"),
    ("Lansia", "usia_lansia", 77.5, "75–80"),
    ("Balita", "usia_balita", 2.5, "1–4"),
    ("Dewasa", "usia_dewasa", 35.0, "25–50"),
]

print("\n=========================================================================")
print("HASIL FUZZIFIKASI")
print("=========================================================================")
print(f"{'No':<4} {'Kategori':<12} {'Usia':<8} {'Interval':<10} {'Fungsi':<24} {'μ(x)':<6}")
print("-------------------------------------------------------------------------")

for idx, (kat, tbl, x, inter) in enumerate(data_uji, start=1):
    cursor = db.cursor()
    cursor.execute(f"SELECT fungsi FROM {tbl} WHERE %s >= b_bawah AND %s <= b_atas", (x, x))
    row = cursor.fetchone()
    fn_name = row[0] if row else "N/A"
    cursor.close()

    mu = fuzzifikasi_usia(tbl, x)
    print(f"{idx:<4} {kat:<12} {x:<8} {inter:<10} {fn_name:<24} {mu:<6}")

print("=========================================================================")

db.close()
