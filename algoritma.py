import time
import copy

from struktur_data import Queue, PriorityQueue


def _bentuk_hasil(hasil, elapsed_detik, operasi_count):
    if hasil:
        rata_tunggu = sum(h.waktu_tunggu() for h in hasil) / len(hasil)
    else:
        rata_tunggu = 0
    return {
        "hasil": hasil,
        "waktu_eksekusi_ms": elapsed_detik * 1000,
        "jumlah_operasi": operasi_count,
        "rata_rata_tunggu": rata_tunggu,
        "jumlah_selesai": len(hasil),
    }


def run_fcfs(dataset):
    data = copy.deepcopy(dataset)
    q = Queue()
    hasil = []
    operasi_count = 0
    waktu_selesai_sebelumnya = 0

    start = time.perf_counter()

    for item in sorted(data, key=lambda x: x.waktu_kedatangan):
        q.enqueue(item)
        operasi_count += 1

    while not q.is_empty():
        current = q.dequeue()
        operasi_count += 1

        waktu_mulai = max(current.waktu_kedatangan, waktu_selesai_sebelumnya)
        waktu_selesai = waktu_mulai + current.estimasi_waktu_layanan

        current.waktu_mulai_layanan = waktu_mulai
        current.waktu_selesai_layanan = waktu_selesai
        current.status = "SELESAI"

        waktu_selesai_sebelumnya = waktu_selesai
        hasil.append(current)

    elapsed = time.perf_counter() - start
    return _bentuk_hasil(hasil, elapsed, operasi_count)


def run_priority(dataset):
    data = copy.deepcopy(dataset)
    pq = PriorityQueue()
    hasil = []
    operasi_count = 0
    waktu_selesai_sebelumnya = 0

    start = time.perf_counter()

    for item in data:
        pq.insert(item, key=(item.prioritas, item.waktu_kedatangan))
        operasi_count += 1

    while not pq.is_empty():
        current = pq.extract_min()
        operasi_count += 1

        waktu_mulai = max(current.waktu_kedatangan, waktu_selesai_sebelumnya)
        waktu_selesai = waktu_mulai + current.estimasi_waktu_layanan

        current.waktu_mulai_layanan = waktu_mulai
        current.waktu_selesai_layanan = waktu_selesai
        current.status = "SELESAI"

        waktu_selesai_sebelumnya = waktu_selesai
        hasil.append(current)

    elapsed = time.perf_counter() - start
    return _bentuk_hasil(hasil, elapsed, operasi_count)
