# Rencana Eksperimen — Minggu 3 (GATE 3)
**Fokus:** Open-Set Rejection, Kalibrasi Ambang Batas ($\tau$), dan Rencana Pengujian Lapangan  
**Target Garis Waktu:** Minggu Ke-3  
**Status Eksekusi:** **BELUM DILAKUKAN (TAHAP MENDATANG / TERJADWAL)**  

---

## Target Rencana Kerja Minggu 3

### 1. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah
* **Tujuan:** Menentukan nilai batas kemiripan (*similarity threshold*) $\tau$ secara objektif tanpa membocorkan data evaluasi (*no data snooping*).
* **Metode Kalibrasi:**
  * Pengujian kurva ROC empiris dan optimasi **Youden's Index ($J = \text{TPR} - \text{FPR}$)** atau **F1-Score Maksimal** pada subset `calibration`.
  * Nilai ambang batas optimal $\tau^*$ yang diperoleh **wajib dibekukan** sebelum evaluasi pada test set.

---

### 2. Eksperimen E3: Evaluasi Penolakan Kelas Terbuka (Open-Set Rejection)
* **Dataset Kontrol Negatif:** Audio fauna non-burung (katak, jangkrik, serangga, kelelawar) dari manifes `unknown_open_set_manifest.csv`.
* **Kriteria Uji:** Audio non-burung harus ditolak jika $\max_{g} \text{Sim}(q, g) < \tau^*$.
* **Pengujian Lintas Derau:** Menguji stabilitas $\tau^*$ beku ketika audio mengalami penurunan SNR hingga -5 dB.

---

### 3. Eksperimen E4: Validasi Soundscape Lapangan ITERA (Studi Eksploratori)
* **Lokasi Pengambilan Sampel:**
  1. Embung ITERA (karakteristik: derau angin terbuka, gemuruh air, serangga air).
  2. Arboretum / Kebun Raya ITERA (karakteristik: gesekan dedaunan, derau jalan raya).
* **Protokol Lapangan:** Mengikuti pedoman teknis pada [`docs/protocols/itera-recording.md`](../../docs/protocols/itera-recording.md).

---

## Kriteria Kelulusan Gate Minggu 3
* Nilai ambang batas $\tau^*$ terbukti stabil dan menolak suara asing dengan False Positive Rate terkontrol.
* Tidak ada data leakage antara partisi kalibrasi dan data uji kueri.

