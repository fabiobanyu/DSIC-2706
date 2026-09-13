# Eksperimen E3 — Open-Set Threshold Evaluation

## 1. Tujuan Ilmiah
Mengevaluasi kestabilan ambang batas kemiripan (similarity threshold $\\tau$) yang dikalibrasi pada kondisi bersih ketika diterapkan untuk menolak sinyal asing (unknown species dan background noise) pada berbagai tingkatan derau.

## 2. Kalibrasi Ambang Batas ($\\tau^*$)
* Dikalibrasi secara eksklusif menggunakan 498 rekaman set kalibrasi (*Strict Calibration Split*).
* Menentukan ambang optimal $\\tau^*$ menggunakan kriteria Youden\'s J pada kurva ROC pada target False Accept Rate (FAR) 5% dan 10%.
* Ambang batas yang diperoleh dibekukan (*frozen threshold*) dan tidak boleh disetel ulang (*re-tuned*) saat pengujian.

## 3. Jenis Sinyal Uji Unknown
1. Unknown mirip: Spesies burung non-target korpus.
2. Unknown non-burung: Suara amfibi, serangga, atau mamalia.
3. Derau murni: Segmen ambient soundscape AudioMoth ITERA tanpa satwa.

## 4. Status Pelaksanaan
**TERJADWAL / BELUM DILAKUKAN** (Tahap Minggu 3 / H15–H21).
