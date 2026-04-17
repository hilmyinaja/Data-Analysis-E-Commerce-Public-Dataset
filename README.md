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

## Kesimpulan
- **Kesimpulan Pertanyaan 1:** Kategori produk security_and_services, diapers_and_hygiene, dan office_furniture memiliki skor ulasan terendah. Tim operasional perlu melakukan inspeksi kualitas pada kategori ini karena tingkat ketidakpuasan pelanggan cukup tinggi.
- **Kesimpulan Pertanyaan 2:** Performa logistik tergolong sangat baik dengan rata-rata waktu pengiriman **11,6 Hari**. Hanya sekitar **6,77%** pesanan yang mengalami keterlambatan dari estimasi awal, menunjukkan sistem penentuan estimasi waktu sudah berjalan efektif.