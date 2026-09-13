# Rencana Eksperimen — Minggu 1 (GATE 1-R)
**Fokus:** Dataset BirdCLEF+ 2026 (20 Spesies Target), Strict Global Recordist-Disjoint Partition, Standardisasi Audio, EDA, E0 (Pipeline Sanity Check), dan E1 (Clean Retrieval Benchmark).  
**Target Garis Waktu:** Minggu Ke-1  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 1-R — 12 September 2026)**

---

## 1. Pembekuan Target Burung, Manifes, & Preprocessing (DEC-09 & DEC-10)

Sesuai arahan Audit Keputusan Kedua tanggal 12 September 2026, eksperimen beralih dari korpus awal 14 spesies manual ke korpus **BirdCLEF+ 2026** guna menjamin daya statistik ($n=200$ kueri bersih) dan independensi rekaman:

* **Spesies Terpilih:** **20 spesies burung Neotropis** (total 4.351 berkas audio fisik) yang lolos seleksi objektif §11.3 (koleksi Xeno-Canto, Aves, rating $\ge 3.0$, klip $\ge 20$, author $\ge 3$). Dari pool 156 kandidat yang lolos ambang, 20 spesies dipilih berdasarkan diversitas perekam tertinggi ($n_{\text{author}} \ge 105$).
* **Transparansi Eksklusi:** 136 spesies kandidat tersisih murni karena kuota 20 taksa, dan 50 spesies tersisih karena kriteria substantif (§11.3), seluruhnya tercatat di `species_excluded.csv`.
* **Parameter Preprocessing Dibekukan:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Durasi Potongan Segmen: **5.0 detik** (160.000 sampel pada jendela energi tertinggi)
  * Normalisasi: RMS Energy Normalization (`target_rms = 0.05`)
  * Transformasi Waktu-Frekuensi: $N_{\text{FFT}} = 1024$, $\text{hop\_length} = 512$
* **Berkas Manifes Kanonikal:**
  * Manifes Spesies Target: [`data/manifests/species_freeze.csv`](../../data/manifests/species_freeze.csv)
  * Manifes Spesies Tereksklusi: [`data/manifests/species_excluded.csv`](../../data/manifests/species_excluded.csv)
  * Manifes Split Bebas Bocor: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Manifes Inventaris BirdCLEF: [`data/manifests/birdclef_inventory.json`](../../data/manifests/birdclef_inventory.json)

---

## 2. Partisi Data Strict Global Recordist-Disjoint (Zero Leakage)

Untuk menjamin evaluasi tidak terdistorsi oleh kesamaan karakteristik perekam (*recorder bias*), pembagian data dilakukan berbasis pengacakan author unik secara global (`seed=42`):

$$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \quad \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \quad \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$$

* **Gallery:** 3.653 rekaman audio dari **377 perekam (*author*) unik**
* **Query Clean:** 200 rekaman audio bersih dari **68 perekam (*author*) unik** (tepat 10 klip per spesies)
* **Calibration:** 498 rekaman audio dari **95 perekam (*author*) unik**
* **Integritas:** Diverifikasi otomatis oleh `tests/test_split_leakage.py` dan `tests/integration/test_split_leakage.py` dengan hasil **0 author overlap, 0 recording ID overlap, dan 0 file path overlap**.

---

## 3. Implementasi Representasi Audio (R0, R1, R2, R3)

Empat representasi audio dievaluasi dengan ekstraksi fitur berdimensi asli dan dinormalisasi L2 unit ($\|\mathbf{x}\|_2 = 1.0$):
1. **$R_0$ (MFCC Baseline):** 40 koefisien spektral + pooling rata-rata/standar deviasi (40-dim).
2. **$R_1$ (Generic Pretrained):** PANNs CNN14 pretrained AudioSet (2048-dim).
3. **$R_2$ (Bioacoustic Domain-Specific):** BirdNET V2.4 Backbone (1024-dim).
4. **$R_3$ (Random Control):** Vektor acak terdistribusi seragam (40-dim, `seed=42`).

Metrik kesamaan dihitung menggunakan **Cosine Similarity** murni.

---

## 4. Hasil Evaluasi Empiris Gate 1-R (Kanonikal & Terverifikasi)

Hasil evaluasi E1 Clean Retrieval Benchmark pada 200 kueri bersih terhadap 3.653 galeri rekaman (tercatat di `results/processed/clean_retrieval_table.csv` dan `paper/tables/clean_retrieval_table.csv`):

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Recall@10 | Precision@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone** | 1024-d | **95.0%** | **0.9126** | **0.9658** | **0.0528** | **0.9280** |
| **$R_1$** | **PANNs CNN14** | 2048-d | **60.0%** | **0.4152** | **0.7005** | **0.0291** | **0.5025** |
| **$R_0$** | **MFCC Baseline** | 40-d | **27.5%** | **0.1319** | **0.4224** | **0.0123** | **0.2175** |
| **$R_3$** | **Random Control** | 40-d | **6.5%** | **0.0190** | **0.1779** | **0.0028** | **0.0530** |

### Analisis Temuan Ilmiah:
1. **Validasi Hipotesis H5 (Kontrol Negatif):** Model terlatih jauh melampaui tebakan acak. Akurasi Top-1 $R_3$ (6.5%) mendekati probabilitas acak teoretis $1/20 = 5.0\%$, membuktikan ketiadaan kebocoran atau jalan pintas (*shortcut learning*).
2. **Hierarki Representasi Bersih:** $R_2\text{ (BirdNET 95.0\%)} > R_1\text{ (PANNs 60.0\%)} > R_0\text{ (MFCC 27.5\%)} \gg R_3\text{ (Random 6.5\%)}$.
3. **Pencatatan Per-Kueri (Audit H5.2):** Berkas [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) menyimpan 800 baris rekaman rinci per kueri lengkap dengan kolom `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, dan `AP@10`.

---

## 5. Notebook Resmi Gate 1-R di `notebooks/`

Direktori `notebooks/` saat ini hanya memuat 4 berkas kanonikal:
1. `notebooks/EDA_Tugas_Akhir.ipynb` — Analisis eksplorasi data & verifikasi kriteria seleksi §11.3.
2. `notebooks/Preprocessing Verification.ipynb` — Validasi pemotongan sinyal 5s dan normalisasi RMS.
3. `notebooks/E0_Pipeline_Sanity_Check.ipynb` — Gerbang anti-kebocoran data dan *smoke test* 4 representasi.
4. `notebooks/E1_Clean_Retrieval.ipynb` — Ekstraksi embedding lengkap dan tolok ukur *clean retrieval*.


---

## 6. Daftar 20 Spesies Target Resmi (`species_freeze.csv`)

| No | Kode Spesies | Nama Ilmiah | Nama Umum | Jumlah Klip | Jumlah Author Unik |
|:---:|:---|:---|:---|:---:|:---:|
| 1 | `coffal1` | *Micrastur semitorquatus* | Collared Forest-Falcon | 253 | 129 |
| 2 | `sobtyr1` | *Camptostoma obsoletum* | Southern Beardless Tyrannulet | 331 | 126 |
| 3 | `greant1` | *Taraba major* | Great Antshrike | 337 | 124 |
| 4 | `squcuc1` | *Piaya cayana* | Common Squirrel-Cuckoo | 332 | 123 |
| 5 | `roahaw` | *Rupornis magnirostris* | Roadside Hawk | 243 | 122 |
| 6 | `trsowl` | *Megascops choliba* | Tropical Screech Owl | 234 | 122 |
| 7 | `banana` | *Coereba flaveola* | Bananaquit | 301 | 121 |
| 8 | `baffal1` | *Micrastur ruficollis* | Barred Forest-Falcon | 273 | 121 |
| 9 | `soulap1` | *Vanellus chilensis* | Southern Lapwing | 243 | 120 |
| 10 | `strcuc1` | *Tapera naevia* | Striped Cuckoo | 250 | 117 |
| 11 | `pabspi1` | *Synallaxis albescens* | Pale-breasted Spinetail | 214 | 117 |
| 12 | `yeofly1` | *Tolmomyias sulphurescens* | Yellow-olive Flatbill | 393 | 115 |
| 13 | `gycwor1` | *Aramides cajaneus* | Grey-cowled Wood Rail | 219 | 115 |
| 14 | `compau` | *Nyctidromus albicollis* | Pauraque | 206 | 115 |
| 15 | `barant1` | *Thamnophilus doliatus* | Barred Antshrike | 294 | 114 |
| 16 | `pirfly1` | *Legatus leucophaius* | Piratic Flycatcher | 288 | 114 |
| 17 | `linwoo1` | *Dryocopus lineatus* | Lineated Woodpecker | 254 | 113 |
| 18 | `whtdov` | *Leptotila verreauxi* | White-tipped Dove | 269 | 111 |
| 19 | `bobfly1` | *Megarynchus pitangua* | Boat-billed Flycatcher | 272 | 107 |
| 20 | `trokin` | *Tyrannus melancholicus* | Tropical Kingbird | 220 | 105 |
