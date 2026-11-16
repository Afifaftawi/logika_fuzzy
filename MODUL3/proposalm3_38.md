PROPOSAL PRODUK SISTEM PENDUKUNG KEPUTUSAN FUZZY
SISTEM PENENTUAN NILAI AKHIR SELEKSI PENERIMAAN MAHASISWA BARU (SIPENA)

   
M. Afif Aftawi (240306038)
Alda Syafitri (2403060 - - )




Program Studi Teknologi Informasi
Fakultas Dakwah dan Ilmu Komunikasi
Universitas Islam Negeri Mataram
2026
1. Latar Belakang dan Problem Statement
1.1 Masalah Nyata yang Ingin Diselesaikan
Proses seleksi penerimaan mahasiswa baru memerlukan penilaian terhadap kemampuan akademik calon mahasiswa berdasarkan kriteria tertentu. Dalam sistem yang dikembangkan, kriteria yang digunakan adalah nilai rapor dan nilai tes tulis dengan rentang nilai 0 sampai 100. Kedua kriteria tersebut digunakan untuk membantu menentukan kelayakan calon mahasiswa baru berdasarkan hasil penilaian akademik.
Permasalahan yang ingin diselesaikan adalah kesulitan dalam melakukan penilaian secara fleksibel ketika nilai calon mahasiswa berada di antara beberapa kategori, seperti rendah, sedang, dan tinggi. Setiap calon mahasiswa juga dapat memiliki kombinasi nilai rapor dan nilai tes tulis yang berbeda. Sebagai contoh, terdapat calon mahasiswa yang memperoleh nilai rapor tinggi tetapi nilai tes tulisnya rendah, atau sebaliknya. Kondisi tersebut membutuhkan metode penilaian yang mampu mempertimbangkan kedua kriteria secara bersamaan untuk menghasilkan nilai akhir seleksi.
Oleh karena itu, diperlukan sistem pendukung keputusan yang dapat membantu mengolah nilai rapor dan nilai tes tulis menjadi hasil penilaian yang lebih terstruktur. Sistem ini dikembangkan menggunakan Logika Fuzzy metode Sugeno Orde 0 untuk menghasilkan nilai akhir seleksi yang dapat digunakan sebagai dasar pemberian rekomendasi keputusan penerimaan mahasiswa baru.
1.2 Mengapa Logika Boolean atau Aturan Kaku Gagal Menyelesaikan Masalah Ini Secara Optimal?
Pendekatan Boolean atau aturan penilaian yang kaku memiliki keterbatasan karena hanya menghasilkan dua kondisi, yaitu benar atau salah, tanpa mempertimbangkan tingkat keanggotaan suatu nilai terhadap beberapa kategori. Dalam proses seleksi, penggunaan batas kategori yang terlalu tegas dapat menyebabkan nilai yang memiliki selisih kecil justru dikelompokkan ke dalam kategori yang berbeda. Padahal, perbedaan nilai tersebut belum tentu menunjukkan perbedaan kemampuan akademik yang signifikan.
Selain itu, pendekatan aturan kaku kurang mampu menggambarkan kondisi ketika suatu nilai memiliki karakteristik yang berada di antara kategori rendah, sedang, dan tinggi. Pendekatan tersebut juga membutuhkan penentuan kondisi yang tegas untuk setiap kombinasi nilai rapor dan nilai tes tulis. Hal ini membuat proses penilaian menjadi kurang fleksibel dalam menghadapi variasi nilai calon mahasiswa.
Untuk mengatasi keterbatasan tersebut, digunakan Logika Fuzzy metode Sugeno Orde 0 yang memungkinkan setiap nilai memiliki derajat keanggotaan antara 0 sampai 1. Melalui fungsi keanggotaan dan sembilan aturan fuzzy, sistem dapat mempertimbangkan kombinasi nilai rapor dan nilai tes tulis secara bersamaan. Hasil perhitungan kemudian diolah menggunakan metode Weighted Average untuk menghasilkan nilai akhir seleksi secara lebih fleksibel dan terstruktur.
1.3 Target Pengguna (Stakeholder) dari Sistem
Target pengguna sistem ini adalah pihak-pihak yang terlibat dalam proses penerimaan mahasiswa baru, khususnya dalam kegiatan penilaian dan pengambilan keputusan seleksi. Stakeholder yang menjadi sasaran pengembangan sistem ini meliputi:
Panitia Seleksi Penerimaan Mahasiswa Baru Merupakan pengguna utama yang bertugas memasukkan nilai rapor dan nilai tes tulis calon mahasiswa ke dalam sistem. Panitia dapat menjalankan proses perhitungan fuzzy serta melihat hasil nilai akhir dan rekomendasi keputusan seleksi.
Bagian Administrasi Penerimaan Mahasiswa Baru Berperan dalam pengelolaan data calon mahasiswa dan hasil penilaian seleksi. Sistem diharapkan dapat membantu penyajian hasil penilaian secara lebih terstruktur sehingga memudahkan proses administrasi.
Pimpinan atau Pihak Pengambil Keputusan Merupakan pihak yang dapat menggunakan hasil perhitungan sistem sebagai bahan pertimbangan dalam proses pengambilan keputusan penerimaan mahasiswa baru. Keputusan akhir tetap berada pada pihak yang memiliki kewenangan dalam proses seleksi.
Dengan adanya sistem ini, setiap stakeholder diharapkan dapat memperoleh informasi hasil penilaian yang lebih terstruktur dan mudah dipahami. Sistem berfungsi sebagai alat bantu pengambilan keputusan, bukan sebagai pengganti kewenangan panitia atau pihak perguruan tinggi dalam menetapkan hasil penerimaan mahasiswa baru.

2. Spesifikasi Variabel Sistem
Variabel	Satuan	Semesta	Label linguistik
Nilai Rapor	Poin	0–100	Rendah, Sedang, Tinggi
Nilai Tes Tulis	Poin	0–100	Rendah, Sedang, Tinggi
Nilai Akhir Seleksi	Poin	20–80	Rendah (20), Sedang (50), Tinggi (80)


3. Rancangan Basis Aturan (Rule Base)
Nilai Rapor \ Nilai Tes Tulis	Rendah	Sedang	Tinggi
Rendah	R1: Rendah	R2: Rendah	R3: Sedang
Sedang	R4: Rendah	R5: Sedang	R6: Tinggi
Tinggi	R7: Sedang	R8: Tinggi	R9: Tinggi
3.1 Tabel Matriks Aturan Kombinatorial
Berikut tabel matriks kombinatorial lengkap dari sembilan aturan fuzzy:

3.2 Daftar Aturan Fuzzy (IF–THEN)
Aturan	Kondisi (IF)	Hasil (THEN)
R1	IF Rapor Rendah AND Tes Tulis Rendah	THEN Nilai Akhir Rendah (20)
R2	IF Rapor Rendah AND Tes Tulis Sedang	THEN Nilai Akhir Rendah (20)
R3	IF Rapor Rendah AND Tes Tulis Tinggi	THEN Nilai Akhir Sedang (50)
R4	IF Rapor Sedang AND Tes Tulis Rendah	THEN Nilai Akhir Rendah (20)
R5	IF Rapor Sedang AND Tes Tulis Sedang	THEN Nilai Akhir Sedang (50)
R6	IF Rapor Sedang AND Tes Tulis Tinggi	THEN Nilai Akhir Tinggi (80)
R7	IF Rapor Tinggi AND Tes Tulis Rendah	THEN Nilai Akhir Sedang (50)
R8	IF Rapor Tinggi AND Tes Tulis Sedang	THEN Nilai Akhir Tinggi (80)
R9	IF Rapor Tinggi AND Tes Tulis Tinggi	THEN Nilai Akhir Tinggi (80)
Berdasarkan tabel matriks tersebut, diperoleh sembilan aturan fuzzy sebagai berikut:

Setiap kategori output pada metode Sugeno Orde 0 direpresentasikan menggunakan nilai konstanta, yaitu:
Rendah = 20 
Sedang = 50 
Tinggi = 80
Kekuatan aktivasi setiap aturan dihitung menggunakan operator AND dengan metode MIN:
  $\alpha_i=\min(\mu_{\text{Rapor}},\mu_{\text{Tes Tulis}})\$

Selanjutnya, nilai akhir seleksi diperoleh melalui metode Weighted Average:
$\[
Z=\frac{\sum_{i=1}^{9}\alpha_i z_i}
{\sum_{i=1}^{9}\alpha_i}
\]$


4. Metode Inferensi & Defuzzifikasi yang Dipilih
Metode inferensi yang digunakan adalah Fuzzy Sugeno Orde 0 (Zero-Order Sugeno). Pemilihan metode ini mengacu pada penelitian Ayuningtias, Irfan, dan Jumadi (2017) yang membahas perbandingan metode Mamdani, Sugeno, dan Tsukamoto dalam kasus prediksi jumlah pendaftar mahasiswa baru.
Metode Sugeno Orde 0 dipilih karena menghasilkan keluaran berupa nilai tegas (crisp) melalui konstanta pada setiap aturan fuzzy. Dalam sistem ini, nilai konsekuen yang digunakan adalah Rendah = 20, Sedang = 50, dan Tinggi = 80. Evaluasi aturan menggunakan operator AND dengan metode MIN.
Proses defuzzifikasi menggunakan metode Weighted Average (rata-rata terbobot) dengan rumus:
$[
Z=\frac{\sum_{i=1}^{n}\alpha_i z_i}
{\sum_{i=1}^{n}\alpha_i}
]$

       

Keterangan: (Z) adalah nilai akhir, (\alpha_i) adalah kekuatan aktivasi aturan, dan (z_i) adalah nilai konstanta setiap aturan.
Secara ilmiah, Sugeno Orde 0 dipilih karena struktur keluarannya sesuai dengan kebutuhan sistem, yaitu menghasilkan nilai akhir seleksi dalam bentuk numerik yang dapat digunakan untuk menentukan keputusan penerimaan mahasiswa. Pemilihan ini didasarkan pada kesesuaian metode dengan kebutuhan sistem, bukan karena Sugeno selalu lebih akurat dibandingkan metode lainnya.
Referensi: Ayuningtias, L. P., Irfan, M., & Jumadi. (2017). Analisa Perbandingan Logic Fuzzy Metode Tsukamoto, Sugeno, dan Mamdani. Jurnal Teknik Informatika, 10(1), 9–16. https://doi.org/10.15408/jti.v10i1.6810
5. Rencana Arsitektur Perangkat Lunak
5.1 Diagram Alur Data
Arsitektur sistem terdiri dari pengguna, antarmuka aplikasi Streamlit, dan modul perhitungan fuzzy. Pengguna memasukkan nilai rapor dan nilai tes tulis. Selanjutnya, sistem memproses data melalui tahapan fuzzifikasi, evaluasi aturan, dan perhitungan Weighted Average hingga menghasilkan nilai akhir serta keputusan seleksi.















5.2 Rencana Implementasi UI (Streamlit)
Antarmuka sistem akan dikembangkan menggunakan Streamlit dengan bahasa pemrograman Python. Implementasi dibagi menjadi dua modul utama:
fuzzy_engine.py: Bertanggung jawab menjalankan proses perhitungan fuzzy, meliputi fuzzifikasi, evaluasi sembilan aturan menggunakan operator AND-MIN, serta perhitungan nilai akhir menggunakan Weighted Average.
app.py: Bertanggung jawab menampilkan antarmuka aplikasi, menerima input nilai rapor dan tes tulis, memanggil modul fuzzy_engine.py, serta menampilkan hasil seleksi.
Data pengujian akan disimpan dalam file test_cases.csv yang berisi contoh nilai rapor dan tes tulis untuk menguji hasil perhitungan sistem.
Antarmuka Streamlit direncanakan memiliki fitur input nilai, tombol proses seleksi, serta tampilan hasil berupa nilai akhir dan status keputusan DITERIMA atau TIDAK DITERIMA.
