# Pembekuan Ruang Lingkup (Scope Freeze) — DSIC-2706

Dokumen ini mencatat batasan ruang lingkup taksonomi, pra-pemrosesan, dan parameter pengujian untuk Tugas Akhir DSIC-2706.

---

## 1. Taksonomi Target (20 Spesies Burung Neotropis Pantanal)

### Amandemen Resmi Bertanggal (Versi 3.0 — 12 September 2026 / Keputusan Kedua)
Berdasarkan audit Gate 1 tanggal 12 September 2026 dan keputusan pembimbing (DEC-09 dan DEC-10), ruang lingkup dataset utama dialihkan ke **BirdCLEF+ 2026 (`train_audio`)** dengan memfilter taksa burung (*Aves*) koleksi Xeno-Canto berkategori rating >= 3.0 serta memilih 20 taksa dengan diversitas perekam unik tertinggi ($N_{\text{author}}$) guna menjamin keabsahan partisi *author-disjoint split*.

Daftar resmi **20 spesies burung target** dengan total **4.351 rekaman audio** terkelola:

| No | Spesies Kunci | Nama Ilmiah | Nama Umum (Inggris) | Jumlah Klip | Jumlah Author | Median Rating |
| :-: | :--- | :--- | :--- | :-: | :-: | :-: |
| 1 | `coffal1` | *Micrastur semitorquatus* | Collared Forest-Falcon | 253 | 129 | 4.0 |
| 2 | `sobtyr1` | *Camptostoma obsoletum* | Southern Beardless Tyrannulet | 331 | 126 | 4.0 |
| 3 | `greant1` | *Taraba major* | Great Antshrike | 337 | 124 | 4.0 |
| 4 | `squcuc1` | *Piaya cayana* | Common Squirrel-Cuckoo | 332 | 123 | 4.0 |
| 5 | `roahaw` | *Rupornis magnirostris* | Roadside Hawk | 243 | 122 | 4.0 |
| 6 | `trsowl` | *Megascops choliba* | Tropical Screech Owl | 234 | 122 | 4.0 |
| 7 | `banana` | *Coereba flaveola* | Bananaquit | 301 | 121 | 4.0 |
| 8 | `baffal1` | *Micrastur ruficollis* | Barred Forest-Falcon | 273 | 121 | 4.0 |
| 9 | `soulap1` | *Vanellus chilensis* | Southern Lapwing | 243 | 120 | 4.5 |
| 10 | `strcuc1` | *Tapera naevia* | Striped Cuckoo | 250 | 117 | 4.0 |
| 11 | `pabspi1` | *Synallaxis albescens* | Pale-breasted Spinetail | 214 | 117 | 4.0 |
| 12 | `yeofly1` | *Tolmomyias sulphurescens* | Yellow-olive Flatbill | 393 | 115 | 4.0 |
| 13 | `gycwor1` | *Aramides cajaneus* | Grey-cowled Wood Rail | 219 | 115 | 4.0 |
| 14 | `compau` | *Nyctidromus albicollis* | Pauraque | 206 | 115 | 4.5 |
| 15 | `barant1` | *Thamnophilus doliatus* | Barred Antshrike | 294 | 114 | 4.0 |
| 16 | `pirfly1` | *Legatus leucophaius* | Piratic Flycatcher | 288 | 114 | 4.0 |
| 17 | `linwoo1` | *Dryocopus lineatus* | Lineated Woodpecker | 254 | 113 | 4.0 |
| 18 | `whtdov` | *Leptotila verreauxi* | White-tipped Dove | 269 | 111 | 4.0 |
| 19 | `bobfly1` | *Megarynchus pitangua* | Boat-billed Flycatcher | 272 | 107 | 4.0 |
| 20 | `trokin` | *Tyrannus melancholicus* | Tropical Kingbird | 220 | 105 | 4.0 |
| **Total** | **20 Spesies** | | | **5.426 Klip Kandidat** | **629 Author Global** | **4.0** |

#### Distribusi Partisi Dataset Split (`data/manifests/dataset_split.csv`):
- **Galeri (*Gallery Bank*):** 3.653 rekaman (377 author independen).
- **Kueri Bersih (*Query Clean*):** Tepat 200 rekaman (20 spesies x 10 kueri per spesies; 68 author independen).
- **Subset Kalibrasi (*Calibration*):** 498 rekaman (95 author independen).
- **Status Kebocoran Perekam:** **Strict Global Author-Disjoint** (0 author tumpang tindih antara Galeri, Kueri, maupun Kalibrasi).

---

### Catatan Historis Ruang Lingkup Sebelumnya
- **Versi 2.0 (07 September 2026):** 16 taksa burung Sumatera (416 rekaman, kurasi manual Xeno-Canto). Dibatalkan oleh audit Gate 1 (12 September 2026) karena kelangkaan data kueri independen ($n=14$), kebocoran perekam (C-04), dan ketergantungan derau sintetis (M-05).
- **Versi 1.0 (Draf Awal):** 16 spesies kosmopolitan umum (digantikan oleh Versi 2.0).

---

## 2. Parameter Pra-pemrosesan Audio (Tetap Dibekukan)
- Laju Sampel (*Sample Rate*): **32.000 Hz** (mono).
- Durasi Segmen: **5.0 detik** (160.000 sampel).
- Seleksi Jendela: **Energi RMS tertinggi (*Top-energy sliding window*)**.
- Normalisasi Energi: **RMS target 0.05** dengan pembatasan puncak kliping <= 1.0.

---

## 3. Tingkat Degradasi Derau Terkontrol (Tetap Dibekukan)
Tingkat degradasi derau aditif dibekukan pada 5 level:
1. **Clean** (SNR = inf)
2. **SNR 20 dB** (Derau ringan)
3. **SNR 10 dB** (Derau sedang)
4. **SNR 0 dB** (Derau berat / sinyal sebanding derau)
5. **SNR -5 dB** (Derau ekstrem / derau melebihi sinyal)

---

## 4. Peran Baru Rekaman AudioMoth Kampus ITERA
Sesuai audit keputusan kedua, rekaman AudioMoth ITERA **tidak lagi menjadi validasi retrieval spesies**, melainkan murni dipersempit menjadi:
1. **Bank derau lingkungan nyata (E2):** Segmen *background-only* bebas vokalisasi burung dari 3 tipe lokasi (Embung, Arboretum, Antropogenik) pada 2 waktu (*daypart*).
2. **Sampel negatif open-set (E3):** Sebagai data uji negatif jenis *pure background*.