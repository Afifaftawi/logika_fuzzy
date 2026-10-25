# ==========================================================
# SISTEM PENENTUAN NILAI AKHIR SELEKSI PENERIMAAN MAHASISWA BARU
# BERBASIS LOGIKA FUZZY
# Praktikum 6: Fuzzy Rule dan Knowledge Base
#
# Cakupan modul ini: basis aturan dan perhitungan firing strength.
# (Fuzzifikasi, agregasi, dan defuzzifikasi dikerjakan di modul berikutnya.)
# ==========================================================


# ==========================================================
# 1. KELAS STRUKTUR ATURAN FUZZY
# ==========================================================
class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator='AND'):
        self.rule_id = rule_id          # nama aturan, mis. "R1"
        self.antecedent = antecedent    # bagian IF: {variabel: label}
        self.consequent = consequent    # bagian THEN: {variabel: label}
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        """Hitung alpha: gabungan derajat keanggotaan semua syarat IF."""
        nilai_derajat = []
        for var_nama, label_nama in self.antecedent.items():
            deg = derajat_fuzzifikasi[var_nama].get(label_nama, 0.0)
            nilai_derajat.append(deg)

        if not nilai_derajat:
            return 0.0

        if self.operator == 'AND':
            return min(nilai_derajat)
        elif self.operator == 'OR':
            return max(nilai_derajat)
        else:
            raise ValueError(f"Operator {self.operator} tidak dikenali.")

    def __str__(self):
        syarat = f" {self.operator} ".join(
            [f"{var} is {lbl}" for var, lbl in self.antecedent.items()])
        hasil = ", ".join(
            [f"{var} is {lbl}" for var, lbl in self.consequent.items()])
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"


# ==========================================================
# 2. BASIS ATURAN (RULE BASE) NILAI AKHIR SELEKSI
#    Variabel input : rapor, tes_tulis  -> Rendah, Sedang, Tinggi
#    Variabel output: nilai_akhir       -> Rendah, Sedang, Tinggi
#    Jumlah aturan  : 3 x 3 = 9
# ==========================================================
rule_base = [
    FuzzyRule("R1", {"rapor": "Rendah", "tes_tulis": "Rendah"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R2", {"rapor": "Rendah", "tes_tulis": "Sedang"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R3", {"rapor": "Rendah", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Sedang"}),
    FuzzyRule("R4", {"rapor": "Sedang", "tes_tulis": "Rendah"}, {"nilai_akhir": "Rendah"}),
    FuzzyRule("R5", {"rapor": "Sedang", "tes_tulis": "Sedang"}, {"nilai_akhir": "Sedang"}),
    FuzzyRule("R6", {"rapor": "Sedang", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Tinggi"}),
    FuzzyRule("R7", {"rapor": "Tinggi", "tes_tulis": "Rendah"}, {"nilai_akhir": "Sedang"}),
    FuzzyRule("R8", {"rapor": "Tinggi", "tes_tulis": "Sedang"}, {"nilai_akhir": "Tinggi"}),
    FuzzyRule("R9", {"rapor": "Tinggi", "tes_tulis": "Tinggi"}, {"nilai_akhir": "Tinggi"}),
]


# ==========================================================
# 3. DATA UJI (DERAJAT KEANGGOTAAN SUDAH DIKETAHUI)
#    Contoh calon mahasiswa: rapor mendekati Sedang/Tinggi,
#    tes tulis dominan Sedang.
# ==========================================================
derajat_input = {
    "rapor":     {"Rendah": 0.0, "Sedang": 0.5,  "Tinggi": 0.5},
    "tes_tulis": {"Rendah": 0.0, "Sedang": 0.75, "Tinggi": 0.25},
}


# ==========================================================
# 4. EVALUASI SELURUH ATURAN
# ==========================================================
print("=" * 86)
print("HASIL EVALUASI BASIS ATURAN FUZZY - NILAI AKHIR SELEKSI MAHASISWA BARU")
print("=" * 86)

aturan_aktif = []
for rule in rule_base:
    alpha = rule.hitung_firing_strength(derajat_input)
    out_var = list(rule.consequent.keys())[0]
    out_lbl = rule.consequent[out_var]
    status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
    print(f"{rule} --> {status}")
    if alpha > 0:
        aturan_aktif.append((rule.rule_id, out_lbl, alpha))

print("\n" + "=" * 86)
print("RINGKASAN ATURAN YANG TERPICU (FIRING RULES):")
print("=" * 86)
for r_id, konklusi, alpha in aturan_aktif:
    print(f" - {r_id:<4}: Nilai Akhir = {konklusi:<8} dengan alpha = {alpha:.2f}")

if not aturan_aktif:
    print(" Tidak ada aturan yang terpicu. Periksa kelengkapan rule base "
          "dan fungsi keanggotaan.")