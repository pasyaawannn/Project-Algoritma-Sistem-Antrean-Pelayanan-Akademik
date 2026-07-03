JENIS_LAYANAN = ["Legalisasi", "Surat Aktif Kuliah", "Konsultasi", "Pengajuan Cuti"]


class PermintaanLayanan:

    def __init__(self, id_mahasiswa, nama, nim, jenis_layanan,
                 prioritas, waktu_kedatangan, estimasi_waktu_layanan):
        self.id_mahasiswa = int(id_mahasiswa)
        self.nama = str(nama).strip()
        self.nim = str(nim).strip()
        self.jenis_layanan = str(jenis_layanan).strip()
        self.prioritas = int(prioritas)
        self.waktu_kedatangan = int(waktu_kedatangan)
        self.estimasi_waktu_layanan = int(estimasi_waktu_layanan)

        self.status = "MENUNGGU"
        self.waktu_mulai_layanan = None
        self.waktu_selesai_layanan = None

    def waktu_tunggu(self):
        if self.waktu_mulai_layanan is None:
            return None
        return self.waktu_mulai_layanan - self.waktu_kedatangan

    def reset_hasil_layanan(self):
        self.status = "MENUNGGU"
        self.waktu_mulai_layanan = None
        self.waktu_selesai_layanan = None

    def to_dict(self):
        return {
            "id_mahasiswa": self.id_mahasiswa,
            "nama": self.nama,
            "nim": self.nim,
            "jenis_layanan": self.jenis_layanan,
            "prioritas": self.prioritas,
            "waktu_kedatangan": self.waktu_kedatangan,
            "estimasi_waktu_layanan": self.estimasi_waktu_layanan,
        }

    def __repr__(self):
        return (f"id={self.id_mahasiswa} | {self.nama} ({self.nim}) | "
                f"{self.jenis_layanan} | prioritas={self.prioritas}")
