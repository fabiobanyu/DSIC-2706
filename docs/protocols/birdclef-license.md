# Protokol Kepatuhan Lisensi Kompetisi BirdCLEF+ 2026 (D-07)

**Topik Riset:** DSIC27-06 — Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Nama Kompetisi:** BirdCLEF+ 2026 — Neotropical Avian & Multi-Taxa Bioacoustic Benchmark  
**Penyelenggara:** LifeCLEF / ImageCLEF & Kaggle  
**URL Resmi:** https://www.kaggle.com/competitions/birdclef-2026/rules  
**Tanggal Akses & Persetujuan:** 12 September 2026  
**Status Keputusan Pembimbing:** D-07 (Disetujui untuk Skripsi & Artikel Ilmiah)

---

## 1. Klausul Penggunaan Non-Komersial & Akademis

Sesuai dengan aturan resmi kompetisi (*Competition Rules Section 7: Use of Data*):
1. **Penggunaan untuk Penelitian Akademis:** Peserta dan akademisi diizinkan mengunduh, mengekstrak, menganalisis, dan memanfaatkan dataset 	rain_audio, 	rain.csv, 	axonomy.csv, dan 	rain_soundscapes untuk tujuan penelitian ilmiah non-komersial, penulisan Tugas Akhir/Skripsi, serta publikasi artikel ilmiah peer-reviewed.
2. **Larangan Penggunaan Komersial:** Dataset tidak boleh diperjualbelikan atau digunakan dalam produk perangkat lunak komersial berbayar tanpa izin tertulis dari pemegang hak cipta.
3. **Larangan Redistribusi Sembarangan:** Audio mentah berukuran besar tidak boleh diredistribusikan secara publik di repositori Git (.gitignore ditegakkan pada folder data/BirdClef/).

---

## 2. Atribusi Sumber Data (Kewajiban Hak Cipta)

Dataset 	rain_audio BirdCLEF+ 2026 bersumber dari repositori bioakustik terbuka:
* **Xeno-Canto Foundation (XC):** Lisensi Creative Commons (CC BY-NC-SA, CC BY-NC-ND, CC BY 4.0).
* **iNaturalist (iNat):** Lisensi Creative Commons dan Public Domain (CC0).

Setiap penggunaan data kueri dan galeri dalam penulisan hasil maupun audit wajib mencantumkan atribusi nama perekam (*author / recordist*) dan ID rekaman unik (*XC ID / filename*), sebagaimana tercatat pada manifes data/manifests/dataset_split.csv.

---

## 3. Batasan terhadap Eksperimen Skripsi
* Penelitian DSIC27-06 **bukan bertujuan mengejar peringkat di leaderboard Kaggle**, melainkan studi ketahanan representasi audio (*audio representation robustness study*) pada kondisi derau dan pergeseran domain.
* Seluruh penggunaan data dibekukan secara deterministik melalui aturan kode pada Gate 1-R.