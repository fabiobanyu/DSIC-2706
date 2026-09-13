# Eksperimen E0 — Pipeline Sanity Check

## 1. Tujuan Ilmiah
Memvalidasi keutuhan jalur pipa komputasi (*pipeline sanity*), memverifikasi ketiadaan kebocoran data (*split leakage*), memastikan stabilitas dimensi fitur serta normalisasi representasi audio (R0, R1, R2, R3), dan menguji hipotesis kontrol negatif H5 sebelum eksperimen skala penuh dijalankan.

## 2. Masukan & Parameter
* **Manifes Data:** `data/manifests/dataset_split.csv` (4.351 baris: 3.653 galeri, 200 kueri bersih, 498 kalibrasi).
* **Standar Audio:** Laju sampel 32.000 Hz, jendela 5.0 detik (160.000 sampel), mono, normalisasi RMS = 0.05.
* **Audio Smoke Test:** Berkas nyata `XC1053050.ogg`.

## 3. Eksekusi Kanonikal
* **Notebook:** [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../../notebooks/E0_Pipeline_Sanity_Check.ipynb)
* **Gerbang Asersi Anti-Bocor:**
  * 0 author overlap antara galeri, kueri bersih, dan kalibrasi (100% *Strict Global Recordist-Disjoint*).
  * 0 recording ID overlap dan 0 file path overlap.
  * Uji kebocoran melempar `AssertionError` jika ada irisan data sekecil apa pun.
* **Smoke Test Dimensi:** R0=(40,), R1=(2048,), R2=(1024,), R3=(40,), seluruhnya bernorma $L_2 = 1.0$ dan bebas NaN/Inf.
* **Verifikasi Kontrol Negatif H5 (Subset 20 Kueri vs 100 Galeri):**
  * $R_2$ (BirdNET): 85.0%
  * $R_1$ (PANNs): 40.0%
  * $R_0$ (MFCC): 5.0%
  * $R_3$ (Random Control): 10.0%

## 4. Status Kelulusan
**LULUS 100% (Gate 1-R)**. Seluruh kriteria dipenuhi tanpa peringatan galat.
