# Research Charter: DSIC-2706

## 1. Metadata Proyek
- **Kode Topik:** DSIC27-06
- **Judul Resmi:** Mencari Audio yang Mirip Ketika Datanya Terbatas
- **Judul Kerja Artikel:** *Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*
- **Peneliti:** Fabio Banyu Cyto (NIM 123450104)
- **Kelompok Riset:** DSIC Research Group — Program Studi Sains Data ITERA
- **Pembimbing:** Dosen Pembimbing Tugas Akhir DSIC

## 2. Latar Belakang & Urgensi
Pemantauan akustik pasif (*passive acoustic monitoring* / PAM) menghasilkan ribuan jam rekaman lingkungan yang tidak beranotasi. Sebagian besar penelitian kecerdasan buatan berfokus pada klasifikasi tertutup (*closed-set classification*), yang mensyaratkan setiap rekaman uji pasti berasal dari kelas latih. Di alam terbuka (khususnya lanskap tropis Sumatera), kondisi nyata melibatkan query langka data, spesies tak terduga (*unknown species*), interferensi derau lingkungan lokal, dan pergeseran domain perekaman dari rekaman fokus (*focal recording*) ke *soundscape* bentang alam.

## 3. Mandat Riset
Penelitian ini memfokuskan diri pada **ketahanan representasi audio untuk pencarian kemiripan (similarity retrieval robustness)**, mengukur representasi mana yang paling lambat kehilangan kemampuan retrieval ketika derau lingkungan meningkat tajam secara berpasangan (*paired stress-testing*).
