# Eksperimen E2 — Controlled Noise Robustness

## 1. Tujuan Ilmiah
Menguji ketahanan (*robustness*) representasi audio ketika kueri bersih mengalami degradasi derau lingkungan tropis nyata pada berbagai tingkatan SNR (+20 dB, +10 dB, 0 dB, -5 dB).

## 2. Sumber Derau & Penghapusan Derau Sintetis
* Sesuai keputusan audit **DEC-09**, derau sintetis pink noise ditinggalkan seutuhnya.
* Menggunakan rekaman suara lingkungan murni (*ambient soundscape*) dari kampus ITERA yang direkam menggunakan perangkat **AudioMoth** (`data/itera_noise/`).
* *Catatan Lapangan:* Perekaman fisik AudioMoth di kampus ITERA dijadwalkan pada Minggu 2 (H8–H14).

## 3. Skema Pengujian Terpasang (*Paired Noise Mixing*)
* 200 kueri bersih yang sama dari E1 dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth.
* Formula pencampuran berbasis daya sinyal eksak:
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$

## 4. Status Pelaksanaan
**TERJADWAL / BELUM DILAKUKAN** (Tahap Minggu 2 / H8–H14).
