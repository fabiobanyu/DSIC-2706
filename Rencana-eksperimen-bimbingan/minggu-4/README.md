# Rencana Eksperimen — Minggu 4 (GATE 4)
**Fokus:** Analisis Kasus Kegagalan, Statistik Inferensial (Bootstrap CI 95%), Penulisan Naskah Skripsi, dan Pembekuan Repositori  
**Target Garis Waktu:** Minggu Ke-4  
**Status Eksekusi:** **BELUM DILAKUKAN (TAHAP MENDATANG / TERJADWAL)**  

---

## Target Rencana Kerja Minggu 4

### 1. Eksperimen E5: Analisis Kasus Kegagalan Temu Kembali (Failure Analysis)
* **Tujuan:** Menambang dan mengaudit kasus-kasus audio kueri nyata yang mengalami kesalahan temu atau penolakan ambang batas keliru.
* **Kategori Kegagalan yang Dianalisis:**
  1. *Low SNR Masking* (harmonik vokal burung tertutup oleh desis/derau).
  2. *Acoustic Feature Overlap* (kemiripan struktur akustik antar spesies berbeda).
  3. *Short Call Duration* (durasi panggilan kicauan terlalu singkat di bawah resolusi jendela waktu).

---

### 2. Evaluasi Statistik Inferensial (Bootstrap Resampling)
* **Tujuan:** Menghitung selang kepercayaan berpasangan (*paired bootstrap confidence interval* 95% CI) melintasi 1.000 iterasi.
* **Uji Signifikansi:** Membuktikan secara statistik apakah keunggulan $R_2$ (BirdNET) atas $R_1$ (PANNs) dan $R_0$ (MFCC) signifikan secara statistik ($p < 0.05$).

---

### 3. Penulisan Naskah Skripsi, Pembekuan Repositori, & Bahan Sidang
* **Penyusunan Bab Skripsi:**
  * Bab 3: Metodologi Penelitian (standarisasi prapemrosesan, pembagian partisi bebas kebocoran, arsitektur representasi).
  * Bab 4: Hasil dan Pembahasan (tabel E1 clean, kurva retensi derau E2, hasil open-set E3).
  * Sub-bab *Threats to Validity*: Batasan penelitian secara transparan dan jujur.
* **Pembekuan Kode (*Code Freeze*):** Menjaga seluruh artefak hasil dan skrip agar dapat direproduksi ulang (*reproducible*) secara deterministik.

