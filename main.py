import glob
import os

from models import PermintaanLayanan, JENIS_LAYANAN
from dataset_io import load_dataset_csv, generate_dataset, save_dataset_csv
from algoritma import run_fcfs, run_priority
from pengujian import uji_algoritma, tampilkan_hasil_uji, tampilkan_perbandingan, ekspor_csv

DATASET_DIR = "dataset"

def input_pilihan_menu(prompt, pilihan_valid):
    while True:
        nilai = input(prompt).strip()
        if nilai in pilihan_valid:
            return nilai
        print(f"[!] Pilihan tidak valid. Pilih salah satu dari: "
              f"{', '.join(sorted(pilihan_valid))}")


def input_teks(prompt):
    nilai = input(prompt).strip()
    if nilai.lower() == "batal":
        return None
    if not nilai:
        print("[!] Input tidak boleh kosong.")
        return input_teks(prompt)
    return nilai


def input_angka(prompt, minimal=None, maksimal=None):
    while True:
        nilai = input(prompt).strip()
        if nilai.lower() == "batal":
            return None
        try:
            angka = int(nilai)
        except ValueError:
            print("[!] Masukkan berupa angka bulat.")
            continue
        if minimal is not None and angka < minimal:
            print(f"[!] Nilai minimal {minimal}.")
            continue
        if maksimal is not None and angka > maksimal:
            print(f"[!] Nilai maksimal {maksimal}.")
            continue
        return angka


def cek_duplikat_nim(dataset, nim):
    for d in dataset:
        if d.nim == nim:
            return d
    return None


def cari_data_by_id(dataset, id_target):
    for d in dataset:
        if d.id_mahasiswa == id_target:
            return d
    return None


def tampilkan_daftar_data(dataset):
    print(f"\n{'ID':<5}{'Nama':<20}{'Jenis Layanan':<20}{'Status':<12}")
    print("-" * 57)
    for d in dataset:
        print(f"{d.id_mahasiswa:<5}{d.nama:<20}{d.jenis_layanan:<20}{d.status:<12}")

def _kunci_urut_dataset(path):
    nama = os.path.basename(path)
    angka = "".join(ch for ch in nama if ch.isdigit())
    return (int(angka) if angka else 0, nama)


def daftar_file_csv():
    if not os.path.isdir(DATASET_DIR):
        return []
    files = glob.glob(os.path.join(DATASET_DIR, "*.csv"))
    return sorted(files, key=_kunci_urut_dataset)


def pilih_dataset_menu(dataset):
    print("\n=== Pilih / Buat Dataset ===")
    file_list = daftar_file_csv()

    if file_list:
        print("Dataset yang tersedia di folder 'dataset/':")
        for i, path in enumerate(file_list, start=1):
            print(f"  {i}. {os.path.basename(path)}")
        idx_generate = len(file_list) + 1
        idx_batal = len(file_list) + 2
        print(f"  {idx_generate}. Generate dataset sintetis baru")
        print(f"  {idx_batal}. Batal")
    else:
        print("  (belum ada file .csv di folder 'dataset/')")
        idx_generate = 1
        idx_batal = 2
        print("  1. Generate dataset sintetis baru")
        print("  2. Batal")

    pilihan_valid = {str(i) for i in range(1, idx_batal + 1)}
    pilihan_int = int(input_pilihan_menu("Pilihan: ", pilihan_valid))

    if pilihan_int == idx_batal:
        print("Dibatalkan.\n")
        return False, None

    if pilihan_int == idx_generate:
        n = input_angka("Jumlah data yang di-generate (mis. 50/100/500/1000): ", 1, None)
        if n is None:
            print("Dibatalkan.\n")
            return False, None
        dataset.clear()
        dataset.extend(generate_dataset(n))
        nama_file = f"dataset_{n}_generated.csv"
        path_simpan = os.path.join(DATASET_DIR, nama_file)
        save_dataset_csv(dataset, path_simpan)
        print(f"[OK] {n} data sintetis berhasil digenerate dan disimpan sebagai "
              f"'{nama_file}'.\n")
        return True, nama_file

    path = file_list[pilihan_int - 1]
    try:
        data, errors = load_dataset_csv(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"[!] {e}\n")
        return False, None

    if not data and not errors:
        print("[!] File ditemukan tapi tidak berisi data.\n")
        return False, None

    dataset.clear()
    dataset.extend(data)
    nama_file = os.path.basename(path)
    print(f"[OK] {len(data)} data berhasil dimuat dari '{nama_file}'.")
    if errors:
        print(f"[!] {len(errors)} baris dilewati karena bermasalah:")
        for nomor, pesan in errors[:5]:
            print(f"    - baris {nomor}: {pesan}")
        if len(errors) > 5:
            print(f"    ... dan {len(errors) - 5} baris lainnya")
    print()
    return True, nama_file


def simpan_sebagai_edited(dataset, file_aktif):
    if file_aktif is None:
        nama_dasar = "dataset_custom"
    else:
        nama_dasar = os.path.splitext(file_aktif)[0]
        if nama_dasar.endswith("_edited"):
            nama_dasar = nama_dasar[: -len("_edited")]
    nama_file_baru = f"{nama_dasar}_edited.csv"
    path_simpan = os.path.join(DATASET_DIR, nama_file_baru)
    save_dataset_csv(dataset, path_simpan)
    return nama_file_baru

def tambah_data(dataset, file_aktif):
    print("\n=== Tambah Data Permintaan Layanan ===")
    print("(ketik 'batal' pada input mana saja untuk kembali ke menu)\n")

    nama = input_teks("Nama mahasiswa : ")
    if nama is None:
        print("Dibatalkan.\n")
        return file_aktif

    while True:
        nim = input_teks("NIM             : ")
        if nim is None:
            print("Dibatalkan.\n")
            return file_aktif

        duplikat = cek_duplikat_nim(dataset, nim)
        if duplikat is None:
            break

        print(f"  [!] NIM '{nim}' sudah terdaftar atas nama "
              f"'{duplikat.nama}' (id {duplikat.id_mahasiswa}).")
        ulang = input_pilihan_menu(
            "      1) Masukkan NIM lain   2) Batalkan penambahan data\n      Pilihan: ",
            {"1", "2"}
        )
        if ulang == "2":
            print("Dibatalkan.\n")
            return file_aktif

    print("\nPilih jenis layanan:")
    for i, jl in enumerate(JENIS_LAYANAN, start=1):
        print(f"  {i}. {jl}")
    idx = input_angka(f"Pilihan (1-{len(JENIS_LAYANAN)}): ", 1, len(JENIS_LAYANAN))
    if idx is None:
        print("Dibatalkan.\n")
        return file_aktif
    jenis_layanan = JENIS_LAYANAN[idx - 1]

    prioritas = input_angka("Prioritas (1=tertinggi ... 4=terendah): ", 1, 4)
    if prioritas is None:
        print("Dibatalkan.\n")
        return file_aktif

    waktu_kedatangan = input_angka("Waktu kedatangan (menit, >=0): ", 0, None)
    if waktu_kedatangan is None:
        print("Dibatalkan.\n")
        return file_aktif

    estimasi = input_angka("Estimasi waktu layanan (menit, >0): ", 1, None)
    if estimasi is None:
        print("Dibatalkan.\n")
        return file_aktif

    id_baru = max((d.id_mahasiswa for d in dataset), default=0) + 1
    item = PermintaanLayanan(id_baru, nama, nim, jenis_layanan,
                              prioritas, waktu_kedatangan, estimasi)
    dataset.append(item)

    file_baru = simpan_sebagai_edited(dataset, file_aktif)
    print(f"\n[OK] Data berhasil ditambahkan dengan id {id_baru}.")
    print(f"[OK] Dataset aktif disimpan sebagai '{file_baru}' "
          f"(file asli '{file_aktif}' tidak diubah).\n")
    return file_baru


def ubah_hapus_data(dataset, file_aktif):
    print("\n=== Ubah / Hapus Data ===")
    if not dataset:
        print("[!] Dataset masih kosong. Pilih/buat dataset terlebih dahulu.\n")
        return file_aktif

    tampilkan_daftar_data(dataset)
    id_target = input_angka("\nMasukkan id data (ketik 'batal' untuk kembali): ", 1, None)
    if id_target is None:
        print("Dibatalkan.\n")
        return file_aktif

    item = cari_data_by_id(dataset, id_target)
    if item is None:
        print(f"[!] Data dengan id {id_target} tidak ditemukan.\n")
        return file_aktif

    aksi = input_pilihan_menu(
        f"\nData ditemukan: {item}\n1) Ubah  2) Hapus  3) Batal\nPilihan: ",
        {"1", "2", "3"}
    )

    if aksi == "3":
        print("Dibatalkan.\n")
        return file_aktif

    if aksi == "2":
        dataset.remove(item)
        file_baru = simpan_sebagai_edited(dataset, file_aktif)
        print(f"[OK] Data id {id_target} berhasil dihapus.")
        print(f"[OK] Dataset aktif disimpan sebagai '{file_baru}' "
              f"(file asli '{file_aktif}' tidak diubah).\n")
        return file_baru

    if item.status != "MENUNGGU":
        print(f"[!] Data berstatus '{item.status}' (sudah pernah diproses "
              f"algoritma), tidak bisa diubah.\n")
        return file_aktif

    print("\nField yang bisa diubah:")
    print("  1. Jenis layanan   2. Prioritas   3. Waktu kedatangan   "
          "4. Estimasi waktu layanan")
    field = input_pilihan_menu("Pilih field (1-4): ", {"1", "2", "3", "4"})

    if field == "1":
        for i, jl in enumerate(JENIS_LAYANAN, start=1):
            print(f"  {i}. {jl}")
        idx = input_angka(f"Jenis layanan baru (1-{len(JENIS_LAYANAN)}): ",
                           1, len(JENIS_LAYANAN))
        if idx is not None:
            item.jenis_layanan = JENIS_LAYANAN[idx - 1]
    elif field == "2":
        nilai = input_angka("Prioritas baru (1-4): ", 1, 4)
        if nilai is not None:
            item.prioritas = nilai
    elif field == "3":
        nilai = input_angka("Waktu kedatangan baru (>=0): ", 0, None)
        if nilai is not None:
            item.waktu_kedatangan = nilai
    elif field == "4":
        nilai = input_angka("Estimasi waktu layanan baru (>0): ", 1, None)
        if nilai is not None:
            item.estimasi_waktu_layanan = nilai

    file_baru = simpan_sebagai_edited(dataset, file_aktif)
    print("[OK] Data berhasil diubah.")
    print(f"[OK] Dataset aktif disimpan sebagai '{file_baru}' "
          f"(file asli '{file_aktif}' tidak diubah).\n")
    return file_baru

def main():
    dataset = []
    file_aktif = None
    hasil_terakhir = {"fcfs": None, "priority": None,
                       "fcfs_dataset": None, "priority_dataset": None}

    menu_teks = """
==================================================
 SISTEM ANTREAN PELAYANAN AKADEMIK
 FCFS vs Priority Scheduling | Queue vs Priority Queue
==================================================
 1. Pilih / Buat Dataset
 2. Tambah Data
 3. Ubah / Hapus Data
 4. Jalankan FCFS (otomatis uji 5x)
 5. Jalankan Priority Scheduling (otomatis uji 5x)
 6. Bandingkan & Rekomendasi
 7. Keluar
--------------------------------------------------
 Jumlah data saat ini : {jumlah}
 Dataset aktif        : {file}
==================================================
"""

    while True:
        print(menu_teks.format(
            jumlah=len(dataset),
            file=file_aktif if file_aktif else "(belum dipilih)"
        ))
        pilihan = input_pilihan_menu(
            "Pilih menu (1-7): ", {str(i) for i in range(1, 8)}
        )

        if pilihan == "1":
            berhasil, nama_file = pilih_dataset_menu(dataset)
            if berhasil:
                file_aktif = nama_file
                hasil_terakhir = {"fcfs": None, "priority": None,
                                   "fcfs_dataset": None, "priority_dataset": None}

        elif pilihan == "2":
            if file_aktif is None and not dataset:
                print("\n[!] Belum ada dataset aktif. Data baru akan disimpan "
                      "sebagai dataset baru bernama 'dataset_custom_edited.csv'.\n")
            file_aktif = tambah_data(dataset, file_aktif)
            hasil_terakhir = {"fcfs": None, "priority": None,
                               "fcfs_dataset": None, "priority_dataset": None}

        elif pilihan == "3":
            file_aktif_baru = ubah_hapus_data(dataset, file_aktif)
            if file_aktif_baru != file_aktif:
                hasil_terakhir = {"fcfs": None, "priority": None,
                                   "fcfs_dataset": None, "priority_dataset": None}
            file_aktif = file_aktif_baru

        elif pilihan == "4":
            if not dataset:
                print("\n[!] Dataset masih kosong. Pilih/buat dataset dulu (menu 1).\n")
                continue
            hasil = uji_algoritma(dataset, run_fcfs)
            tampilkan_hasil_uji("FCFS", hasil)
            path_csv = ekspor_csv("FCFS", file_aktif, hasil)
            print(f"[OK] Hasil pengujian ditambahkan ke: {path_csv}\n")
            hasil_terakhir["fcfs"] = hasil
            hasil_terakhir["fcfs_dataset"] = file_aktif

        elif pilihan == "5":
            if not dataset:
                print("\n[!] Dataset masih kosong. Pilih/buat dataset dulu (menu 1).\n")
                continue
            hasil = uji_algoritma(dataset, run_priority)
            tampilkan_hasil_uji("Priority Scheduling", hasil)
            path_csv = ekspor_csv("Priority Scheduling", file_aktif, hasil)
            print(f"[OK] Hasil pengujian ditambahkan ke: {path_csv}\n")
            hasil_terakhir["priority"] = hasil
            hasil_terakhir["priority_dataset"] = file_aktif

        elif pilihan == "6":
            fcfs_ok = (hasil_terakhir["fcfs"] is not None
                       and hasil_terakhir["fcfs_dataset"] == file_aktif)
            prio_ok = (hasil_terakhir["priority"] is not None
                       and hasil_terakhir["priority_dataset"] == file_aktif)

            if not (fcfs_ok and prio_ok):
                print("\n[!] Jalankan menu 4 (FCFS) DAN menu 5 (Priority Scheduling) "
                      "terlebih dahulu pada dataset aktif yang sama sebelum "
                      "membandingkan.\n")
                continue

            print()
            tampilkan_perbandingan(hasil_terakhir["fcfs"], hasil_terakhir["priority"])

        elif pilihan == "7":
            print("Terima kasih, program selesai.")
            break


if __name__ == "__main__":
    main()
