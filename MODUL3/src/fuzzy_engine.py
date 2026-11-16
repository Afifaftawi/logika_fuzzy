def rendah(x, a, b):
    if x <= a:
        return 1
    elif x >= b:
        return 0
    else:
        return (b - x) / (b - a)

def sedang(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

def tinggi(x, a, b):
    if x <= a:
        return 0
    elif x >= b:
        return 1
    else:
        return (x - a) / (b - a)

def fuzzifikasi_rapor(nilai):
    return {
        "Rendah": rendah(nilai, 50, 80),
        "Sedang": sedang(nilai, 50, 70, 90),
        "Tinggi": tinggi(nilai, 60, 90)
    }

def fuzzifikasi_tes(nilai):
    return {
        "Rendah": rendah(nilai, 40, 80),
        "Sedang": sedang(nilai, 40, 65, 90),
        "Tinggi": tinggi(nilai, 50, 90)
    }

def hitung_fuzzy(nilai_rapor, nilai_tes_tulis):

    rapor = fuzzifikasi_rapor(nilai_rapor)
    tes = fuzzifikasi_tes(nilai_tes_tulis)

    aturan = [
        ("Rendah", "Rendah", 20),
        ("Rendah", "Sedang", 20),
        ("Rendah", "Tinggi", 50),
        ("Sedang", "Rendah", 20),
        ("Sedang", "Sedang", 50),
        ("Sedang", "Tinggi", 80),
        ("Tinggi", "Rendah", 50),
        ("Tinggi", "Sedang", 80),
        ("Tinggi", "Tinggi", 80)
    ]

    total_alpha = 0
    total_hasil = 0
    detail_aturan = []

    for i, aturan_data in enumerate(aturan):
        label_rapor, label_tes, konstanta = aturan_data

        alpha = min(
            rapor[label_rapor],
            tes[label_tes]
        )

        total_alpha += alpha
        total_hasil += alpha * konstanta

        detail_aturan.append({
            "aturan": "R" + str(i + 1),
            "alpha": alpha,
            "konstanta": konstanta
        })


    if total_alpha == 0:
        nilai_akhir = 0
    else:
        nilai_akhir = total_hasil / total_alpha


    if nilai_akhir >= 60:
        keputusan = "DITERIMA"
    else:
        keputusan = "TIDAK DITERIMA"

    return {
        "nilai_akhir": nilai_akhir,
        "keputusan": keputusan,
        "detail_aturan": detail_aturan
    }
