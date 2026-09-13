# Rencana Eksperimen — Minggu 2 (GATE 2)
**Fokus:** Akuisisi Data Lapangan AudioMoth ITERA & Controlled Noise Robustness (Paired SNR Stress-Testing)  
**Target Garis Waktu:** Minggu Ke-2 (H8–H14)  
**Status Eksekusi:** **TERJADWAL / BELUM DILAKUKAN (Menunggu Perekaman Fisik Lapangan AudioMoth)**  

---

## 1. Perekaman Fisik AudioMoth di Kampus ITERA (H8–H13)
* **Status Lapangan:** **Belum Dilakukan**. Unit AudioMoth dijadwalkan dipasang di kampus ITERA pada Minggu 2.
* **Titik Penempatan:**
  1. *Titik Vegetasi/Embung:* Ambien alam, biophony serangga/jangkrik, gemerisik dedaunan, dan angin.
  2. *Titik Antropogenik:* Dekat koridor gedung/jalan kampus untuk menangkap derau aktivitas manusia dan kendaraan.
* **Konfigurasi AudioMoth:** Sample rate 32.000 Hz, gain medium, interval perekaman kontinu/berkala. Salinan berkas `CONFIG.TXT` wajib disimpan di repositori.
* **Kurasi Segmen Derau Murni (H13):** Memotong segmen 5,0 detik yang dipastikan **bebas dari suara burung target korpus** dan menyimpannya di `data/itera_noise/`.
* **Pembersihan Jalur Derau Sintetis:** Sesuai mandat DEC-09, derau sintetis (*pink noise*) ditinggalkan seutuhnya. Fungsi cadangan pada `src/mix_noise.py` akan diubah menjadi galat fatal (`raise FileNotFoundError`) saat data AudioMoth dimasukkan.

---

## 2. Eksperimen E2: Evaluasi Temu Kembali di Bawah Derau (H11–H13)
* **Kueri Terpasang:** 200 kueri bersih dari E1 dicampur dengan segmen derau AudioMoth yang sama menggunakan seed tetap (`seed=42`).
* **Grid SNR Terkontrol:**
  1. *Clean:* Kondisi dasar tanpa derau (baseline E1)
  2. *SNR +20 dB:* Derau latar sangat ringan
  3. *SNR +10 dB:* Derau latar sedang
  4. *SNR 0 dB:* Daya sinyal dan derau berimbang
  5. *SNR -5 dB:* Derau dominan terhadap sinyal vokal
* **Formulasi Pencampuran Eksak:**
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$
* **Model yang Dievaluasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 Generic Audio (2048-dim)
  * $R_2$: BirdNET Backbone Bioacoustic (1024-dim)
  * $R_3$: Random Control (40-dim)

---

## 3. Kriteria Kelulusan Gate 2 (H14)
- [ ] Bank derau `data/itera_noise/` terisi audio rekaman nyata AudioMoth dan lolos verifikasi ketiadaan burung target.
- [ ] Manifes `data/manifests/itera_noise_manifest.csv` terisi lengkap dan di-checksum SHA-256.
- [ ] Fallback pink noise di `src/mix_noise.py` dihapus.
- [ ] Pemasangan kueri ke segmen derau bersifat deterministik.
- [ ] Kurva degradasi $mAP@10$ dan retensi relatif terhadap SNR dihasilkan tanpa artefak *ceiling*/*floor*.
- [ ] Seluruh log pemeringkatan per-kueri mentah tersimpan secara terstruktur di `results/raw/`.
