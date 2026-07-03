# Sistem Antrean Pelayanan Akademik

Project Analisis Algoritma — Topik 2: Sistem Antrean Pelayanan Akademik
Perbandingan algoritma **FCFS (First Come First Served)** vs **Priority
Scheduling**, menggunakan struktur data **Queue** dan **Priority Queue**
(binary min-heap).

## Cara Menjalankan

Pastikan Python 3.8 ke atas sudah terpasang, tidak ada dependensi tambahan
(hanya modul bawaan Python).

```bash
cd sistem_antrean
python main.py
```

## Struktur Folder

```
sistem_antrean/
├── main.py            -> menu utama & alur program
├── models.py           -> definisi objek PermintaanLayanan
├── struktur_data.py     -> implementasi manual Queue & Priority Queue
├── algoritma.py          -> implementasi FCFS & Priority Scheduling
├── dataset_io.py          -> load/simpan CSV & generator dataset sintetis
├── pengujian.py             -> uji otomatis 5x, rata-rata, export CSV
├── README.md
├── dataset/                  -> dataset skala 50 / 100 / 500 / 1000
│   ├── dataset_50.csv
│   ├── dataset_100.csv
│   ├── dataset_500.csv
│   └── dataset_1000.csv
└── hasil_pengujian/            -> (dibuat otomatis) rekap CSV hasil uji
    └── rekap_pengujian.csv
```

## Menu Program

1. **Pilih / Buat Dataset** — memuat salah satu file CSV di `dataset/`,
   atau generate dataset sintetis baru dengan skala bebas.
2. **Tambah Data** — menambah satu permintaan layanan baru ke dataset aktif.
3. **Ubah / Hapus Data** — mengubah atau menghapus data berdasarkan id.
4. **Jalankan FCFS (otomatis uji 5x)** — menjalankan algoritma FCFS
   sebanyak 5x berturut-turut pada dataset aktif (sesuai ketentuan panduan
   project), menampilkan ringkasan (rata-rata waktu tunggu, rata-rata
   waktu eksekusi, jumlah operasi, jumlah layanan selesai) di atas, lalu
   tabel waktu eksekusi tiap percobaan (Uji 1–5) di bawahnya. Hasil otomatis
   diekspor ke CSV.
5. **Jalankan Priority Scheduling (otomatis uji 5x)** — sama seperti di
   atas, untuk algoritma Priority Scheduling.
6. **Bandingkan & Rekomendasi** — menampilkan tabel perbandingan FCFS vs
   Priority Scheduling berdampingan beserta rekomendasi otomatis. Hanya bisa
   dijalankan setelah menu 4 dan 5 dijalankan pada dataset aktif yang sama.
7. **Keluar**

## Catatan Penting: Dataset Aktif & Penyimpanan

- Saat program pertama kali dibuka, dataset aktif **kosong** — pilih dulu
  lewat menu 1.
- Perubahan lewat menu 2 (Tambah) atau 3 (Ubah/Hapus) **tidak pernah
  menimpa file asli**. Hasilnya otomatis disimpan sebagai file baru
  berlabel `_edited` (misalnya `dataset_50_edited.csv`), sehingga file
  dataset asli (50/100/500/1000) selalu tetap bersih untuk pengujian ulang
  dari awal.
- FCFS dan Priority Scheduling selalu memproses **satu dataset aktif** saat
  itu (satu skala per waktu), bukan gabungan seluruh file dataset.

## Catatan Penting: Waktu Eksekusi

Waktu eksekusi diukur memakai `time.perf_counter()` — pengukuran waktu
nyata (real-time) saat program berjalan, bukan angka tetap. Nilainya **wajar
berbeda-beda** setiap kali dijalankan, dan berbeda pula antar perangkat,
karena dipengaruhi beban CPU/sistem operasi saat itu. Untuk mengurangi noise
ini, menu 4 dan 5 **otomatis menjalankan algoritma 5x** dan merata-ratakan
hasilnya, sesuai ketentuan panduan project (Table 5): "Setiap skenario diuji
minimal lima kali dan digunakan nilai rata-rata."

## Menjalankan Pengujian untuk Laporan

Untuk mengisi tabel hasil pengujian di laporan (skala 50, 100, 500, 1000):

1. Menu 1 → pilih `dataset_50.csv`
2. Menu 4 → FCFS otomatis diuji 5x, hasil tercetak dan tersimpan ke
   `hasil_pengujian/rekap_pengujian.csv`
3. Menu 5 → Priority Scheduling otomatis diuji 5x, hasil tercetak dan
   tersimpan ke file CSV yang sama
4. Menu 6 → lihat tabel perbandingan FCFS vs Priority Scheduling
5. Ulangi langkah 1–4 untuk `dataset_100.csv`, `dataset_500.csv`,
   `dataset_1000.csv`
6. Buka `hasil_pengujian/rekap_pengujian.csv` di Excel/Google Sheets untuk
   menyusun tabel akhir dan membuat grafik perbandingan
