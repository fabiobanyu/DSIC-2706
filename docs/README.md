# Dokumentasi Metodologi & Riset Tugas Akhir (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Status Terkini:** Revisi Audit Gate 1-R Selesai 100% (12 September 2026)  

---

## 1. Ringkasan Eksekutif Riset

Penelitian ini mengevaluasi **ketahanan representasi audio beku (*frozen representations*) untuk temu kembali kemiripan (*similarity retrieval*)** ketika kueri bioakustik mengalami penurunan kualitas akibat derau lingkungan tropis dan pergeseran domain:

* **Representasi Audio yang Dibandingkan:**
  * $R_0$: MFCC Baseline (40-dim, *handcrafted acoustic*)
  * $R_1$: PANNs CNN14 (2048-dim, *generic deep audio embedding*)
  * $R_2$: BirdNET V2.4 Backbone (1024-dim, *domain-specific bioacoustic representation*)
  * $R_3$: Random Control (40-dim, *negative control baseline*)
* **Korpus Galeri & Kueri (DEC-09 / Gate 1-R):** Menggunakan subset terkurasi **BirdCLEF+ 2026** lintas 20 spesies burung Neotropis (total 4.351 berkas audio fisik) dengan pembagian *Strict Global Recordist-Disjoint*:
  * Galeri: 3.653 rekaman audio (377 perekam unik)
  * Kueri Bersih: 200 rekaman audio (68 perekam unik, 10 klip/spesies)
  * Kalibrasi Open-Set: 498 rekaman audio (95 perekam unik)
* **Derau Lapangan Terkontrol:** Menggunakan rekaman langsung perangkat **AudioMoth** dari kampus ITERA (`data/itera_noise/`), derau sintetis pink noise ditinggalkan sepenuhnya. *(Catatan: Perekaman fisik AudioMoth dijadwalkan pada Minggu 2 / H8–H14).*
* **Hasil Tolok Ukur Bersih E1:** $R_2\text{ (BirdNET 95.0\%)} > R_1\text{ (PANNs 60.0\%)} > R_0\text{ (MFCC 27.5\%)} \gg R_3\text{ (Random 6.5\%)}$.
* **Integritas Suite Uji:** Seluruh 9 unit test saintifik pada `run_tests.py` lulus 100.0%.

---

## 2. Indeks Dokumen Penelitian di `docs/`

### A. Kebijakan, Ruang Lingkup, & Batasan Ilmiah (`docs/research/`)
1. [`research-charter.md`](./research/research-charter.md) — Piagam penelitian, batasan masalah, dan tujuan utama.
2. [`rq.md`](./research/rq.md) — Rincian Pertanyaan Penelitian (RQ Utama dan Sub-RQ).
3. [`hypotheses.md`](./research/hypotheses.md) — 5 Hipotesis kerja ilmiah ($H_1$ s.d. $H_5$).
4. [`novelty-boundary.md`](./research/novelty-boundary.md) — Batasan kebaruan dan kontribusi ilmiah spesifik.
5. [`scope-freeze.md`](./research/scope-freeze.md) — Pembekuan ruang lingkup korpus Versi 3.0 (BirdCLEF+ 2026, 20 taksa beku).
6. [`decision-log.md`](./research/decision-log.md) — Register keputusan formal riset (DEC-01 hingga DEC-10).

### B. Protokol Metodologis & Pengujian (`docs/protocols/`)
1. [`itera-recording.md`](./protocols/itera-recording.md) — Panduan penempatan, konfigurasi, dan kurasi derau AudioMoth ITERA.
2. [`open-set.md`](./protocols/open-set.md) — Prosedur kalibrasi ambang batas $\tau^*$ menggunakan Youden's J pada target FAR 5% dan 10%.
3. [`birdclef-license.md`](./protocols/birdclef-license.md) — Klausul kepatuhan lisensi kompetisi BirdCLEF untuk penggunaan akademik dan skripsi.
4. [`annotation.md`](./protocols/annotation.md) — Standar anotasi rekaman bentang suara (*soundscapes*).
5. [`xeno-canto-selection.md`](./protocols/xeno-canto-selection.md) — Kriteria awal penyaringan rekaman audio.

---

## 3. Rekam Jejak Pelaksanaan & Logbook

Seluruh rekam jejak revisi bimbingan, matriks audit, log eksekusi terminal, dan data numerik empiris tercatat lengkap dan transparan pada:  
👉 **[`Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md`](../Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md)**
