# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) dan rekam jejak bimbingan untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**  
*Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)
* **Status Terkini:** Minggu Ke-1 (GATE 1-R) Selesai 100% per 12 September 2026 (Pivot BirdCLEF+ 2026, 20 Spesies, 4.351 Klip Audio, E0 & E1 Lolos). Minggu 2 s.d 4 Terjadwal (Menunggu Perekaman Lapangan AudioMoth ITERA).

---

### Dokumen Rekam Jejak Revisi & Progres:
Seluruh catatan kemajuan, audit metodologi, dan bukti numerik tercatat secara kronologis di:  
👉 **[CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md)**

---

## Peta Navigasi Rencana Eksperimen & Status Gate

| Direktori Rencana | Fokus & Target Mingguan | Status Pelaksanaan | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset BirdCLEF+ 2026 (20 Spesies), Standarisasi Audio (32 kHz, 5s, RMS 0.05), EDA, E0 (Pipeline Sanity), dan E1 (Clean Retrieval) | **SELESAI 100% (GATE 1-R LOLOS)**<br>• 20 Spesies Target (4.351 Berkas Audio)<br>• Strict Recordist-Disjoint (0 Overlap Author, ID, Path)<br>• $R_2$ (BirdNET) 95.0% > $R_1$ 60.0% > $R_0$ 27.5% >> $R_3$ 6.5%<br>• Suite Uji Saintifik: 9/9 PASS (100.0%) | [Buka Dokumen Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Akuisisi Derau Lapangan AudioMoth ITERA & Controlled Noise Robustness (Eksperimen E2: Paired Stress-Testing pada SNR +20, +10, 0, -5 dB) | **TERJADWAL (BELUM DILAKUKAN)**<br>*(Menunggu perekaman fisik AudioMoth ITERA / H8–H14)* | [Buka Rencana Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection & Kalibrasi Ambang Batas $\tau$ (Eksperimen E3) serta Domain Shift Real Soundscape (E4) | **TERJADWAL (BELUM DILAKUKAN)**<br>*(Terjadwal untuk Minggu Ke-3)* | [Buka Rencana Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Analisis Kasus Kegagalan (E5), Statistik Inferensial (Bootstrap CI 95%), Naskah Skripsi, & Freeze Code | **TERJADWAL (BELUM DILAKUKAN)**<br>*(Terjadwal untuk Minggu Ke-4)* | [Buka Rencana Minggu 4](./minggu-4/README.md) |

---

## Hubungan Terhadap Tahapan Bimbingan

Dokumentasi di folder `Rencana-eksperimen-bimbingan/` ini menjadi bukti fisik terverifikasi:

* **Tahap 1 (Dataset 20 Spesies BirdCLEF+, Manifes Bebas Bocor, & Baseline E0/E1):** Telah selesai di [Minggu 1](./minggu-1/README.md).
* **Tahap 2 (Akuisisi AudioMoth ITERA & Ketahanan Derau E2):** Dirancang pada [Minggu 2](./minggu-2/README.md).
* **Tahap 3 (Open-Set & Kalibrasi $\tau$ E3):** Dirancang pada [Minggu 3](./minggu-3/README.md).
* **Tahap 4 (Evaluasi Lengkap & Naskah Akhir):** Dirancang pada [Minggu 4](./minggu-4/README.md).

