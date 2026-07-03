import csv
import os
import random

from models import PermintaanLayanan

KOLOM_WAJIB = {
    "id_mahasiswa", "nama", "nim", "jenis_layanan",
    "prioritas", "waktu_kedatangan", "estimasi_waktu_layanan",
}

BOBOT_JENIS_LAYANAN = {
    "Legalisasi": 0.4,
    "Surat Aktif Kuliah": 0.2,
    "Konsultasi": 0.2,
    "Pengajuan Cuti": 0.2,
}


def load_dataset_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File dataset tidak ditemukan: '{path}'")

    dataset = []
    error_list = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if not KOLOM_WAJIB.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"Format CSV tidak sesuai. Kolom wajib: {sorted(KOLOM_WAJIB)}"
            )

        nim_terlihat = set()
        for nomor_baris, row in enumerate(reader, start=2):  # baris 1 = header
            try:
                nim = str(row["nim"]).strip()
                if nim in nim_terlihat:
                    error_list.append(
                        (nomor_baris, f"NIM {nim} duplikat di dalam file, baris dilewati")
                    )
                    continue

                item = PermintaanLayanan(
                    id_mahasiswa=row["id_mahasiswa"],
                    nama=row["nama"],
                    nim=nim,
                    jenis_layanan=row["jenis_layanan"],
                    prioritas=row["prioritas"],
                    waktu_kedatangan=row["waktu_kedatangan"],
                    estimasi_waktu_layanan=row["estimasi_waktu_layanan"],
                )
                dataset.append(item)
                nim_terlihat.add(nim)
            except (ValueError, KeyError) as e:
                error_list.append((nomor_baris, str(e)))

    return dataset, error_list


def generate_dataset(n, id_mulai=1, seed=None):
    if seed is not None:
        random.seed(seed)

    nama_depan = ["Umi", "Dewi", "Qori", "Hadi", "Fani", "Zainal", "Rini",
                  "Wahyu", "Bambang", "Lestari", "Citra", "Dedi", "Andi", "Rizki"]
    nama_belakang = ["Pratama", "Kusuma", "Santoso", "Saputra", "Handayani",
                      "Wijaya", "Putri", "Siregar", "Nugroho", "Ramadhan"]

    jenis_list = list(BOBOT_JENIS_LAYANAN.keys())
    bobot_list = list(BOBOT_JENIS_LAYANAN.values())

    dataset = []
    nim_terpakai = set()
    for i in range(n):
        nama = f"{random.choice(nama_depan)} {random.choice(nama_belakang)}"

        while True:
            nim = str(random.randint(202600001, 202699999))
            if nim not in nim_terpakai:
                nim_terpakai.add(nim)
                break

        jenis = random.choices(jenis_list, weights=bobot_list, k=1)[0]
        prioritas = random.randint(1, 4)
        waktu_kedatangan = random.randint(0, max(n * 2, 10))
        estimasi = random.randint(5, 30)

        item = PermintaanLayanan(
            id_mahasiswa=id_mulai + i,
            nama=nama,
            nim=nim,
            jenis_layanan=jenis,
            prioritas=prioritas,
            waktu_kedatangan=waktu_kedatangan,
            estimasi_waktu_layanan=estimasi,
        )
        dataset.append(item)

    return dataset


def save_dataset_csv(dataset, path):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    fieldnames = ["id_mahasiswa", "nama", "nim", "jenis_layanan",
                  "prioritas", "waktu_kedatangan", "estimasi_waktu_layanan"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in dataset:
            writer.writerow(item.to_dict())
