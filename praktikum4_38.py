import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. FUNGSI KEANGGOTAAN (MEMBERSHIP FUNCTIONS)
# ---------------------------------------------------------
def trimf(x, params):
    """Fungsi keanggotaan Segitiga [a, b, c]"""
    a, b, c = params
    return np.maximum(0.0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

def trapmf(x, params):
    """Fungsi keanggotaan Trapesium [a, b, c, d]"""
    a, b, c, d = params
    term1 = (x - a) / (b - a)
    term2 = (d - x) / (d - c)
    return np.maximum(0.0, np.minimum(term1, np.minimum(1.0, term2)))

# ---------------------------------------------------------
# 2. DEFINISI OPERATOR FUZZY
# ---------------------------------------------------------
def tnorm_min(mu_a, mu_b):
    return np.minimum(mu_a, mu_b)

def tnorm_product(mu_a, mu_b):
    return mu_a * mu_b

def tconorm_max(mu_a, mu_b):
    return np.maximum(mu_a, mu_b)

def tconorm_algebraic_sum(mu_a, mu_b):
    return mu_a + mu_b - (mu_a * mu_b)

def fuzzy_not(mu):
    return 1.0 - mu

# ---------------------------------------------------------
# 3. DOMAIN SEMESTA & PENETAPAN HIMPUNAN A DAN B
# ---------------------------------------------------------
x = np.linspace(0, 100, 1000)

# Himpunan A: Bandwidth Cukup [30, 60, 90] (Segitiga)
mu_a = trimf(x, [30, 60, 90])

# Himpunan B: Packet Loss Rendah / Throughput Efektif [40, 55, 75, 95] (Trapesium)
mu_b = trapmf(x, [40, 55, 75, 95])

# ---------------------------------------------------------
# 4. HASIL OPERASI PADA SEMESTA KONTINU
# ---------------------------------------------------------
intersection_min = tnorm_min(mu_a, mu_b)
intersection_prod = tnorm_product(mu_a, mu_b)
union_max = tconorm_max(mu_a, mu_b)
union_alg = tconorm_algebraic_sum(mu_a, mu_b)
not_a = fuzzy_not(mu_a)

# ---------------------------------------------------------
# 5. VISUALISASI HASIL OPERASI
# ---------------------------------------------------------
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Graph 1: Himpunan A, B, dan NOT A
axes[0].plot(x, mu_a, label='A (Bandwidth Cukup)', color='#1f77b4', linewidth=2)
axes[0].plot(x, mu_b, label='B (Packet Loss Rendah)', color='#ff7f0e', linewidth=2)
axes[0].plot(x, not_a, label='NOT A (Komplemen A)', color='gray', linestyle='--', linewidth=1.5)
axes[0].set_title('1. Himpunan Fuzzy A, B, dan Komplemen NOT A', fontweight='bold')
axes[0].set_ylabel('μ(x)')
axes[0].grid(True, linestyle=':', alpha=0.6)
axes[0].legend()

# Graph 2: Perbandingan Intersection (AND)
axes[1].plot(x, intersection_min, label='Zadeh Min (A ∩ B)', color='#2ca02c', linewidth=2)
axes[1].plot(x, intersection_prod, label='Algebraic Product (A · B)', color='#d62728', linestyle='-.', linewidth=2)
axes[1].set_title('2. Komparasi Operasi Intersection (T-Norm / AND)', fontweight='bold')
axes[1].set_ylabel('μ(x)')
axes[1].grid(True, linestyle=':', alpha=0.6)
axes[1].legend()

# Graph 3: Perbandingan Union (OR)
axes[2].plot(x, union_max, label='Zadeh Max (A ∪ B)', color='#9467bd', linewidth=2)
axes[2].plot(x, union_alg, label='Algebraic Sum (A + B - A·B)', color='#8c564b', linestyle='-.', linewidth=2)
axes[2].set_title('3. Komparasi Operasi Union (T-Conorm / OR)', fontweight='bold')
axes[2].set_xlabel('Throughput / Bandwidth (Mbps)')
axes[2].set_ylabel('μ(x)')
axes[2].grid(True, linestyle=':', alpha=0.6)
axes[2].legend()

plt.tight_layout()
plt.savefig('tugas_praktikum4_bandwidth.png', dpi=300)
plt.show()
