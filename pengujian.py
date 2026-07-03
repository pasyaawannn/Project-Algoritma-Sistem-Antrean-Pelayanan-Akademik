import os
import csv
import statistics

JUMLAH_PERCOBAAN = 5
HASIL_DIR = "hasil_pengujian"


def uji_algoritma(dataset, fungsi_algoritma, jumlah_percobaan=JUMLAH_PERCOBAAN):
    waktu_list = []
    hasil_terakhir = None
    for _ in range(jumlah_percobaan):
        hasil_terakhir = fungsi_algoritma(dataset)
        waktu_list.append(hasil_terakhir["waktu_eksekusi_ms"])

    return {
        "percobaan_ms": waktu_list,
        "rata_rata_ms": statistics.mean(waktu_list),
        "rata_rata_tunggu": hasil_terakhir["rata_rata_tunggu"],
        "jumlah_operasi": hasil_terakhir["jumlah_operasi"],
        "jumlah_selesai": hasil_terakhir["jumlah_selesai"],
    }


def tampilkan_hasil_uji(nama_algoritma, r):
    print(f"\n=== Hasil Pengujian: {nama_algoritma} (5x) ===")
    print(f"  Rata-rata waktu tunggu   : {r['rata_rata_tunggu']:.2f} menit")
    print(f"  Waktu eksekusi           : {r['rata_rata_ms']:.4f} ms (rata-rata dari 5x)")
    print(f"  Jumlah operasi struktur  : {r['jumlah_operasi']}")
    print(f"  Jumlah layanan selesai   : {r['jumlah_selesai']}")

    print(f"\n  {'Percobaan':<15}{'Waktu Eksekusi (ms)':<22}")
    print("  " + "-" * 37)
    for i, ms in enumerate(r["percobaan_ms"], start=1):
        print(f"  {'Uji ' + str(i):<15}{ms:<22.4f}")
    print(f"  {'Rata-rata':<15}{r['rata_rata_ms']:<22.4f}")
    print()


def tampilkan_perbandingan(hasil_fcfs, hasil_priority):
    print("=== Tabel Perbandingan FCFS vs Priority Scheduling ===\n")
    print(f"{'Metrik':<32}{'FCFS':<18}{'Priority':<18}")
    print("-" * 68)
    print(f"{'Rata-rata waktu eksekusi (ms)':<32}{hasil_fcfs['rata_rata_ms']:<18.4f}"
          f"{hasil_priority['rata_rata_ms']:<18.4f}")
    print(f"{'Rata-rata waktu tunggu (menit)':<32}{hasil_fcfs['rata_rata_tunggu']:<18.2f}"
          f"{hasil_priority['rata_rata_tunggu']:<18.2f}")
    print(f"{'Jumlah operasi struktur data':<32}{hasil_fcfs['jumlah_operasi']:<18}"
          f"{hasil_priority['jumlah_operasi']:<18}")
    print(f"{'Jumlah layanan selesai':<32}{hasil_fcfs['jumlah_selesai']:<18}"
          f"{hasil_priority['jumlah_selesai']:<18}")

    print("\n=== Rekomendasi Otomatis (berdasarkan hasil di atas) ===")
    if hasil_priority["rata_rata_tunggu"] < hasil_fcfs["rata_rata_tunggu"]:
        print("-> Priority Scheduling memberikan rata-rata waktu tunggu LEBIH RENDAH")
        print("   pada dataset ini. Cocok dipakai jika prioritas layanan (mis. cuti")
        print("   mendesak) penting, dengan trade-off kompleksitas O(log n) per operasi")
        print("   (dibanding O(1) pada FCFS).")
    elif hasil_priority["rata_rata_tunggu"] > hasil_fcfs["rata_rata_tunggu"]:
        print("-> FCFS memberikan rata-rata waktu tunggu LEBIH RENDAH pada dataset ini.")
        print("   FCFS lebih sederhana (O(1) per operasi) dan cukup adil jika prioritas")
        print("   antar permintaan tidak terlalu bervariasi.")
    else:
        print("-> Kedua algoritma menghasilkan rata-rata waktu tunggu yang sama pada")
        print("   dataset ini.")
    print("\n[Catatan] Rekomendasi final untuk laporan sebaiknya didiskusikan bersama")
    print("kelompok, mempertimbangkan hasil pada seluruh skala data (50/100/500/1000),")
    print("bukan hanya satu dataset saja.\n")


def ekspor_csv(nama_algoritma, nama_dataset, r):
    os.makedirs(HASIL_DIR, exist_ok=True)
    path = os.path.join(HASIL_DIR, "rekap_pengujian.csv")
    file_sudah_ada = os.path.exists(path)

    kolom_uji = [f"uji_{i+1}_ms" for i in range(len(r["percobaan_ms"]))]
    fieldnames = (["dataset", "algoritma"] + kolom_uji +
                  ["rata_rata_ms", "rata_rata_tunggu_menit",
                   "jumlah_operasi", "jumlah_selesai"])

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_sudah_ada:
            writer.writeheader()

        baris = {"dataset": nama_dataset, "algoritma": nama_algoritma}
        for i, ms in enumerate(r["percobaan_ms"]):
            baris[f"uji_{i+1}_ms"] = f"{ms:.4f}"
        baris["rata_rata_ms"] = f"{r['rata_rata_ms']:.4f}"
        baris["rata_rata_tunggu_menit"] = f"{r['rata_rata_tunggu']:.2f}"
        baris["jumlah_operasi"] = r["jumlah_operasi"]
        baris["jumlah_selesai"] = r["jumlah_selesai"]
        writer.writerow(baris)

    return path
