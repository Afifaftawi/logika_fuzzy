class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator='AND'):
        """
        antecedent: dict berisi pasangan {'nama_variabel': 'nama_label'}
        consequent: dict berisi {'nama_variabel': 'nama_label'}
        """
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        """
        Menghitung nilai firing strength (alpha-predikat)
        menggunakan operator Zadeh (AND = min, OR = max)
        """
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
        syarat = f" {self.operator} ".join([f"{var} is {lbl}" for var, lbl in self.antecedent.items()])
        hasil = ", ".join([f"{var} is {lbl}" for var, lbl in self.consequent.items()])
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"

rule_base = [
    FuzzyRule("R1", {"suhu": "Dingin", "cpu": "Ringan"}, {"kipas": "Lambat"}),
    FuzzyRule("R2", {"suhu": "Dingin", "cpu": "Sedang"}, {"kipas": "Lambat"}),
    FuzzyRule("R3", {"suhu": "Dingin", "cpu": "Berat"}, {"kipas": "Sedang"}),
    FuzzyRule("R4", {"suhu": "Normal", "cpu": "Ringan"}, {"kipas": "Lambat"}),
    FuzzyRule("R5", {"suhu": "Normal", "cpu": "Sedang"}, {"kipas": "Sedang"}),
    FuzzyRule("R6", {"suhu": "Normal", "cpu": "Berat"}, {"kipas": "Cepat"}),
    FuzzyRule("R7", {"suhu": "Panas", "cpu": "Ringan"}, {"kipas": "Sedang"}),
    FuzzyRule("R8", {"suhu": "Panas", "cpu": "Sedang"}, {"kipas": "Cepat"}),
    FuzzyRule("R9", {"suhu": "Panas", "cpu": "Berat"}, {"kipas": "Cepat"}),
]

print("=" * 60)
print("MASUKKAN NILAI DERAJAT FUZZIFIKASI INPUT (Rentang 0.0 s.d 1.0)")
print("=" * 60)

try:
    print("\n--- Variabel Suhu Ruang ---")
    suhu_dingin = float(input("Masukkan derajat Suhu [Dingin]: "))
    suhu_normal = float(input("Masukkan derajat Suhu [Normal]: "))
    suhu_panas  = float(input("Masukkan derajat Suhu [Panas] : "))

    print("\n--- Variabel Beban CPU ---")
    cpu_ringan = float(input("Masukkan derajat CPU [Ringan]: "))
    cpu_sedang = float(input("Masukkan derajat CPU [Sedang]: "))
    cpu_berat  = float(input("Masukkan derajat CPU [Berat] : "))

    derajat_input_manual = {
        "suhu": {"Dingin": suhu_dingin, "Normal": suhu_normal, "Panas": suhu_panas},
        "cpu": {"Ringan": cpu_ringan, "Sedang": cpu_sedang, "Berat": cpu_berat}
    }

except ValueError:
    print("\n[Kesalahan] Harap masukkan angka desimal yang valid (contoh: 0.5 atau 1.0).")
    exit()
    
print("\n" + "=" * 75)
print("HASIL EVALUASI BASIS ATURAN FUZZY - KIPAS PENDINGIN SERVER")
print("=" * 75)

aturan_aktif = []
for rule in rule_base:
    alpha = rule.hitung_firing_strength(derajat_input_manual)
    output_var = list(rule.consequent.keys())[0]
    output_lbl = rule.consequent[output_var]
    status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
    print(f"{rule} --> {status}")
    if alpha > 0:
        aturan_aktif.append((rule.rule_id, output_lbl, alpha))

print("\n" + "=" * 75)
print("RINGKASAN ATURAN YANG TEPICU (FIRING RULES):")
print("=" * 75)
if aturan_aktif:
    for r_id, konklusi, alpha in aturan_aktif:
        print(f" - {r_id:<4} : Kecepatan Kipas = {konklusi:<8} dengan alpha = {alpha:.2f}")
else:
    print(" Tidak ada aturan yang aktif (semua alpha = 0.0).")