# Praktikum 6 — Fuzzy Rule dan Knowledge Base
## Perancangan Aturan Proposisi IF-THEN, Basis Pengetahuan, dan Evaluasi Firing Strength dengan Python

---

## A. Tujuan Praktikum
Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Memahami konsep struktur proposisi aturan fuzzy: bagian *Antecedent* (premis/kondisi) dan *Consequent* (konklusi/tindakan).
2. Menyusun basis aturan (*Rule Base*) dan basis pengetahuan (*Knowledge Base*) berdasarkan logika pakar atau karakteristik domain masalah.
3. Menghitung nilai kekuatan pemicu (*Firing Strength* / $\alpha$-predikat) untuk aturan berkondisi majemuk (menggunakan operator AND/OR).
4. Mengimplementasikan struktur data Rule Base dalam bahasa pemrograman Python.
5. Melakukan pengujian evaluasi aturan terhadap berbagai kombinasi input data.
6. Menganalisis kondisi aktivasi aturan (*rule firing*) serta teknik menangani aturan yang tidak aktif.

---

## B. Konsep Dasar

### 1. Struktur Aturan Fuzzy IF-THEN
Aturan fuzzy dinyatakan dalam bentuk penalaran logis manusia (*linguistic rules*):

$$\textbf{IF } x \text{ is } A \textbf{ AND } y \text{ is } B \textbf{ THEN } z \text{ is } C$$

Di mana:
- **Antecedent (Premis):** Bagian kondisi yang berada di antara `IF` dan `THEN` (contoh: $x \text{ is } A \text{ AND } y \text{ is } B$).
- **Consequent (Konklusi):** Bagian keputusan yang berada setelah `THEN` (contoh: $z \text{ is } C$).
- $x, y$ adalah variabel linguistik input, sedangkan $z$ adalah variabel linguistik output.
- $A, B, C$ adalah label-label linguistik.

```text
               ANTECEDENT / PREMIS                             CONSEQUENT / KESIMPULAN
┌──────────────────────────────────────────────┐              ┌────────────────────────┐
│ IF Waktu_Tunggu is LAMA AND Urgensi is TINGGI │ ──────────►  │ THEN Prioritas is TOP  │
└──────────────────────────────────────────────┘              └────────────────────────┘
```

### 2. Nilai Kekuatan Pemicu (*Firing Strength* / $\alpha$-predikat)
Ketika suatu nilai input crisp dimasukkan ke dalam sistem, setiap aturan akan menghasilkan derajat kebenaran premis yang disebut **Firing Strength** ($\alpha$):
- Jika antecedent menggunakan operator **AND** (konjungsi):
  $$\alpha_i = \min(\mu_{A_i}(x), \mu_{B_i}(y)) \quad \text{atau} \quad \alpha_i = \mu_{A_i}(x) \cdot \mu_{B_i}(y)$$
- Jika antecedent menggunakan operator **OR** (disjungsi):
  $$\alpha_i = \max(\mu_{A_i}(x), \mu_{B_i}(y))$$

### 3. Matriks Basis Aturan (*Rule Matrix*)
Jika terdapat dua variabel input:
- Variabel 1 memiliki $m$ label linguistik.
- Variabel 2 memiliki $n$ label linguistik.

Maka total kombinasi aturan lengkap (*complete rule base*) adalah $m \times n$ aturan.

*Contoh Matriks Aturan (Prioritas Tiket Helpdesk):*
| Waktu Tunggu \ Urgensi | Rendah | Sedang | Tinggi |
|---|---|---|---|
| **Cepat** | R1: Rendah | R2: Rendah | R3: Sedang |
| **Sedang** | R4: Rendah | R5: Sedang | R6: Tinggi |
| **Lama** | R7: Sedang | R8: Tinggi | R9: Kritis |

---

## C. Contoh Perhitungan Manual Firing Strength

Misalkan sebuah tiket bantuan memiliki data input:
- Nilai keanggotaan `Waktu Tunggu`:
  - $\mu_{\text{Cepat}} = 0.0$
  - $\mu_{\text{Sedang}} = 0.4$
  - $\mu_{\text{Lama}} = 0.6$
- Nilai keanggotaan `Urgensi Tiket`:
  - $\mu_{\text{Rendah}} = 0.0$
  - $\mu_{\text{Sedang}} = 0.7$
  - $\mu_{\text{Tinggi}} = 0.3$

Mari hitung nilai pemicu ($\alpha$) untuk beberapa aturan yang relevan menggunakan operator Zadeh Min:

1. **Aturan 5 (R5):**
   $$\textbf{IF } \text{Waktu is Sedang AND Urgensi is Sedang} \textbf{ THEN } \text{Prioritas is Sedang}$$
   $$\alpha_5 = \min(\mu_{\text{Sedang}}(Waktu), \mu_{\text{Sedang}}(Urgensi)) = \min(0.4, 0.7) = \mathbf{0.4}$$

2. **Aturan 6 (R6):**
   $$\textbf{IF } \text{Waktu is Sedang AND Urgensi is Tinggi} \textbf{ THEN } \text{Prioritas is Tinggi}$$
   $$\alpha_6 = \min(\mu_{\text{Sedang}}(Waktu), \mu_{\text{Tinggi}}(Urgensi)) = \min(0.4, 0.3) = \mathbf{0.3}$$

3. **Aturan 8 (R8):**
   $$\textbf{IF } \text{Waktu is Lama AND Urgensi is Sedang} \textbf{ THEN } \text{Prioritas is Tinggi}$$
   $$\alpha_8 = \min(\mu_{\text{Lama}}(Waktu), \mu_{\text{Sedang}}(Urgensi)) = \min(0.6, 0.7) = \mathbf{0.6}$$

4. **Aturan 9 (R9):**
   $$\textbf{IF } \text{Waktu is Lama AND Urgensi is Tinggi} \textbf{ THEN } \text{Prioritas is Kritis}$$
   $$\alpha_9 = \min(\mu_{\text{Lama}}(Waktu), \mu_{\text{Tinggi}}(Urgensi)) = \min(0.6, 0.3) = \mathbf{0.3}$$

Aturan lainnya menghasilkan $\alpha = 0.0$ karena salah satu operand bernilai 0.

---

## D. Implementasi dalam Python

Simpan script berikut sebagai `pertemuan6_fuzzy_rule.py`:

```python
# ==========================================================
# 1. KELAS STRUKTUR ATURAN FUZZY
# ==========================================================
class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator='AND'):
        """
        antecedent: dict berisi pasangan {'nama_variabel': 'nama_label'}
                    contoh: {'waktu': 'Sedang', 'urgensi': 'Tinggi'}
        consequent: dict berisi {'nama_variabel': 'nama_label'}
                    contoh: {'prioritas': 'Tinggi'}
        """
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        """
        derajat_fuzzifikasi: dict bersarang berisi derajat keanggotaan input,
        contoh: {'waktu': {'Cepat': 0.0, 'Sedang': 0.4, 'Lama': 0.6},
                 'urgensi': {'Rendah': 0.0, 'Sedang': 0.7, 'Tinggi': 0.3}}
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


# ==========================================================
# 2. INISIALISASI BASIS ATURAN (RULE BASE)
# ==========================================================
rule_base = [
    FuzzyRule("R1", {"waktu": "Cepat", "urgensi": "Rendah"}, {"prioritas": "Rendah"}),
    FuzzyRule("R2", {"waktu": "Cepat", "urgensi": "Sedang"}, {"prioritas": "Rendah"}),
    FuzzyRule("R3", {"waktu": "Cepat", "urgensi": "Tinggi"}, {"prioritas": "Sedang"}),
    FuzzyRule("R4", {"waktu": "Sedang", "urgensi": "Rendah"}, {"prioritas": "Rendah"}),
    FuzzyRule("R5", {"waktu": "Sedang", "urgensi": "Sedang"}, {"prioritas": "Sedang"}),
    FuzzyRule("R6", {"waktu": "Sedang", "urgensi": "Tinggi"}, {"prioritas": "Tinggi"}),
    FuzzyRule("R7", {"waktu": "Lama", "urgensi": "Rendah"}, {"prioritas": "Sedang"}),
    FuzzyRule("R8", {"waktu": "Lama", "urgensi": "Sedang"}, {"prioritas": "Tinggi"}),
    FuzzyRule("R9", {"waktu": "Lama", "urgensi": "Tinggi"}, {"prioritas": "Kritis"}),
]


# ==========================================================
# 3. EVALUASI ATURAN TERHADAP DATA INPUT
# ==========================================================
derajat_input_sampel = {
    "waktu": {"Cepat": 0.0, "Sedang": 0.4, "Lama": 0.6},
    "urgensi": {"Rendah": 0.0, "Sedang": 0.7, "Tinggi": 0.3}
}

print("=" * 75)
print("HASIL EVALUASI BASIS ATURAN FUZZY")
print("=" * 75)

aturan_aktif = []
for rule in rule_base:
    alpha = rule.hitung_firing_strength(derajat_input_sampel)
    output_var = list(rule.consequent.keys())[0]
    output_lbl = rule.consequent[output_var]
    status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
    print(f"{rule} --> {status}")
    if alpha > 0:
        aturan_aktif.append((rule.rule_id, output_lbl, alpha))

print("\n" + "=" * 75)
print("RINGKASAN ATURAN YANG TEPICU (FIRING RULES):")
print("=" * 75)
for r_id, konklusi, alpha in aturan_aktif:
    print(f" - {r_id:<4} : Prioritas = {konklusi:<8} dengan alpha = {alpha:.2f}")
```

---

## E. Skenario Pengujian Basis Aturan

Ujilah basis aturan di atas untuk 3 skenario kondisi operasional yang berbeda:

| Skenario | Deskripsi Kasus | Fuzzifikasi Waktu | Fuzzifikasi Urgensi | Daftar Aturan yang Terpicu | Nilai Alpha |
|:--:|---|---|---|---|---|
| **A** | Masalah Baru Masuk & Ringan | Cepat: 1.0, Lainnya: 0.0 | Rendah: 0.8, Sedang: 0.2, Tinggi: 0.0 | R1, R2 | $\alpha_1=0.8, \alpha_2=0.2$ |
| **B** | Kasus Antrean Sedang & Mendesak | Sedang: 0.7, Lama: 0.3 | Sedang: 0.4, Tinggi: 0.6 | R5, R6, R8, R9 | $\alpha_5=0.4, \alpha_6=0.6, \alpha_8=0.3, \alpha_9=0.3$ |
| **C** | Masalah Kritis Lama Mengendap | Lama: 1.0, Lainnya: 0.0 | Tinggi: 1.0, Lainnya: 0.0 | R9 | $\alpha_9=1.0$ |

---

## F. Tugas Praktikum 6

### Kasus: Sistem Kendali Kipas Pendingin Server Ruang Data
Dua variabel input digunakan:
1. `Suhu Ruang` (3 label: *Dingin, Normal, Panas*).
2. `Beban CPU` (3 label: *Ringan, Sedang, Berat*).

Variabel output:
- `Kecepatan Kipas` (3 label: *Lambat, Sedang, Cepat*).

**Instruksi:**
1. Rancang tabel matriks basis aturan ($3 \times 3 = 9$ aturan) secara logis.
2. Buat program Python untuk mendefinisikan ke-9 aturan tersebut.
3. Jalankan pengujian evaluasi aturan untuk input:
   - Suhu: `Dingin: 0.2, Normal: 0.8, Panas: 0.0`
   - Beban CPU: `Ringan: 0.0, Sedang: 0.5, Berat: 0.5`
4. Tampilkan daftar aturan yang aktif beserta nilai firing strength $\alpha$-nya.

---

## G. Pertanyaan Analisis

1. Apa yang akan terjadi pada sistem inferensi fuzzy jika suatu kombinasi input tidak memicu satu pun aturan ($\alpha_i = 0$ untuk semua $i$)? Bagaimana cara mencegah kondisi tersebut (*completeness of rule base*)?
2. Jika dua aturan yang aktif menghasilkan konklusi yang sama (misalnya R6 dan R8 sama-sama menghasilkan *Prioritas = Tinggi*), bagaimanakah kedua nilai $\alpha$ tersebut digabungkan pada tahap agregasi?
3. Mengapa urutan aturan (*rule ordering*) pada basis aturan fuzzy tidak memengaruhi hasil akhir sistem? Jelaskan perbedaan karakteristik ini dibandingkan struktur `if-elif-else` imperatif!

---

## H. Ketentuan & Pengumpulan
1. Mahasiswa mengumpulkan script Python `Modul-2/Praktikum6_<NIM>.py`.
2. Commit git: `feat(modul2): implementasi basis aturan dan firing strength praktikum 6`.

---

## I. Kesimpulan
Basis aturan fuzzy merepresentasikan kepakaran manusia ke dalam bentuk formal komputasi. Setiap aturan mengevaluasi derajat kecocokan kondisinya secara independen dan paralel melalui nilai *firing strength* $\alpha$. Tahap evaluasi aturan ini menjadi jembatan krusial antara input fuzzifikasi dan pembentukan output keputusan pada Fuzzy Inference System.
