# E-Commerce Data Dashboard

Dashboard ini dibuat untuk menganalisis performa e-commerce publik, mencakup kualitas produk, efisiensi logistik pengiriman, dan segmentasi pelanggan (RFM Analysis).

## Setup environment
Pastikan sudah menginstal pipenv di komputer anda. Jika belum, instal menggunakan command:
```bash
pip install pipenv
```

Setelah itu ketik command:
```bash
mkdir analisis_data_ecommerce
cd analisis_data_ecommerce
pipenv install -r requirements.txt
pipenv shell
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```

### Mengumpulkan Data
Pada tahap ini, kita memuat 9 dataset E-Commerce. Dataset ini mencakup seluruh siklus pesanan mulai dari profil pelanggan, detail barang, ulasan, hingga rekam jejak logistik pengiriman.

### Menilai Data
Dari hasil pengecekan .info(), .isna(), dan .duplicated(), ditemukan beberapa masalah:
1. Kolom tanggal pada orders_df masih bertipe object (string) dan perlu diubah ke datetime.
2. Terdapat *missing values* pada tanggal pengiriman pelanggan di orders_df.
3. Terdapat produk tanpa nama kategori di products_df.

### Membersihkan Data
Langkah pembersihan yang dilakukan:
1. Mengubah tipe data seluruh kolom waktu menjadi datetime agar bisa dihitung selisihnya.
2. Menghapus baris pesanan yang tidak memiliki tanggal sampai ke pelanggan (*drop missing values*).
3. Mengisi *missing values* pada kategori produk dengan label "unknown" agar tidak mengganggu agregasi data.

### Eksplorasi Data
Tahap ini menggabungkan (*merge*) tabel ulasan, produk, dan pesanan untuk mencari rata-rata skor ulasan per kategori. Selain itu, dilakukan perhitungan matematika untuk mencari durasi aktual pengiriman dan selisihnya dengan waktu estimasi.

### Visualisasi Data
Membuat visualisasi Bar Chart untuk melihat kategori produk terburuk, serta Histogram untuk melihat distribusi lama waktu pengiriman kepada pelanggan.

### Analisis Lanjutan: RFM (Recency, Frequency, Monetary)
Melakukan segmentasi pelanggan untuk mengidentifikasi siapa pelanggan yang paling baru berbelanja (Recency), paling sering berbelanja (Frequency), dan menghabiskan uang paling banyak (Monetary).

## Kesimpulan dan Rekomendasi

**1. Kategori produk apa yang memiliki rata-rata skor ulasan terendah selama periode 2017-2018?**
* **Kesimpulan:** Berdasarkan analisis ulasan, kategori security_and_services mencetak skor terendah (rata-rata 2.50), diikuti oleh diapers_and_hygiene (3.25), dan office_furniture (3.49). Kategori perabotan kantor sangat kritis karena memiliki volume ulasan yang masif (1.687 ulasan).
* **Rekomendasi:** Tim Quality Control (QC) harus segera melakukan audit menyeluruh terhadap vendor yang mensuplai kategori office_furniture. Mengingat dimensinya yang besar, disarankan untuk mengevaluasi prosedur packing untuk mengurangi potensi kerusakan barang saat pengiriman yang memicu kekecewaan pelanggan.

**2. Bagaimana performa logistik (waktu pengiriman dan keterlambatan) pada tahun 2018?**
* **Kesimpulan:** Secara keseluruhan, rata-rata waktu pengiriman dari pembayaran hingga tiba di tangan pelanggan adalah 11,64 hari. Sistem logistik tergolong andal dengan hanya 6,77% pesanan yang melampaui batas estimasi pengiriman.
* **Rekomendasi:** Perusahaan sebaiknya mempertahankan algoritma penentuan batas waktu estimasi saat ini karena berhasil membuat mayoritas pelanggan menerima barang lebih cepat. Untuk menekan angka 6,77% keterlambatan, tim logistik bisa memprioritaskan rute ekspedisi pada rute-rute long-tail yang sering memakan waktu di atas 30 hari.

**3. Bagaimana segmentasi pelanggan berdasarkan RFM di tahun 2018?**
* **Kesimpulan:** Analisis RFM menunjukkan ketimpangan yang signifikan pada Prinsip Pareto. Mayoritas pelanggan hanya melakukan 1 kali transaksi, namun terdapat segelintir pelanggan loyal (seperti ID awalan 8d50f5...) yang bertransaksi hingga lebih dari 20 kali, serta "Whales" yang menyumbang pendapatan di atas 100.000 BRL.
* **Rekomendasi:** Fokus tim Marketing harus digeser dari Customer Acquisition menjadi Customer Retention dengan membuat program Loyalty/VIP Tier eksklusif bagi pelanggan dengan nilai Monetary dan Frequency tinggi untuk memastikan mereka tidak beralih ke kompetitor.