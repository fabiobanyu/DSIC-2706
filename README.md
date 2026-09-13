# DSIC-2706 — Robust Bioacoustic Similarity Retrieval under Noise and Domain Shift

Repositori penelitian untuk topik **DSIC-2706: Mencari Audio yang Mirip Ketika Datanya Terbatas**.

Fokus penelitian ini bukan membuat classifier spesies baru, melainkan menguji **ketahanan representasi audio untuk similarity retrieval** ketika query mengalami derau lingkungan dan pergeseran domain dari *focal recording* ke *real soundscape*.

Judul kerja artikel yang direkomendasikan:

> **Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise**

## 1. Pertanyaan penelitian

### RQ utama

**Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik mengalami peningkatan derau lingkungan dan pergeseran domain dari focal recording ke soundscape?**

### Sub-RQ

1. Seberapa besar penurunan `mAP@k` dan `Recall@k` untuk setiap representasi pada beberapa tingkat SNR yang dibentuk menggunakan background noise ITERA?
2. Apakah threshold kemiripan yang dikalibrasi pada data terpisah tetap mampu menolak *unknown species* dan *background noise* ketika tingkat noise dan domain perekaman berubah?
3. Apakah *bioacoustic-specific embedding* memiliki *robustness retention* yang lebih baik daripada *generic pretrained audio embedding* dan MFCC pada kondisi noise yang sama?
4. Sebagai analisis sekunder, candidate match spesies apa yang muncul pada subset soundscape ITERA yang telah diverifikasi manual?

## 2. Hipotesis

- **H1 — Robustness retention:** deep pretrained representation mempertahankan proporsi `mAP@k` yang lebih besar daripada MFCC ketika SNR diturunkan.
- **H2 — Domain-specific advantage:** bioacoustic embedding mengalami penurunan retrieval yang lebih kecil daripada generic audio embedding pada query burung dengan environmental noise.
- **H3 — Domain shift:** kinerja pada real soundscape turun lebih besar daripada controlled mixture pada SNR sebanding karena domain shift tidak hanya berupa additive noise.
- **H4 — Threshold transfer:** threshold yang baik pada calibration-clean tidak selalu stabil ketika kondisi noise berubah.
- **H5 — Positive control:** clean retrieval harus mengungguli random ranking. Jika tidak, pipeline harus diaudit sebelum hasil diinterpretasikan.

Semua hipotesis boleh ditolak. Hasil nol tetap merupakan hasil penelitian apabila eksperimen, kontrol, dan confidence interval valid.

## 3. Batas kontribusi

Kontribusi ilmiah utama:

- evaluasi *paired robustness* pada query yang sama;
- controlled environmental-noise stress test menggunakan background ITERA;
- perbandingan hand-crafted, generic pretrained, dan bioacoustic pretrained representation;
- kurva degradasi retrieval terhadap SNR;
- pengujian transfer threshold pada open-set condition;
- validasi eksternal pada real ITERA soundscape.

Yang **bukan** kontribusi utama:

- membuat model BirdNET/PANNs baru;
- fine-tuning banyak model;
- classifier fauna baru;
- occupancy modelling;
- abundance estimation;
- inventarisasi biodiversitas kampus secara lengkap;
- dashboard atau aplikasi produksi.

## 4. Representasi yang dibandingkan

| Kode | Representasi | Dimensi | Peran | Checkpoint / Sumber |
|---|---|---|---|---|
| **R0** | MFCC (40 koefisien + delta + delta-delta, mean/std pooling) | 40-d | Baseline akustik klasik | `librosa` feature extractor |
| **R1** | PANNs CNN14 (AudioSet general audio pretrained) | 2048-d | Deep embedding generik | `checkpoints/Cnn14_mAP=0.431.pth` |
| **R2** | BirdNET Backbone (Avian bioacoustic domain pretrained) | 1024-d | Domain-specific representation | Pustaka `birdnet` resmi |
| **R3** | Random Control (Vektor acak terdistribusi seragam) | 40-d | Negative control | Deterministik (`seed=42`) |

Semua representasi utama dinormalisasi ke *unit sphere* (\(\|\mathbf{x}\|_2 = 1.0\)) dan dievaluasi menggunakan **cosine similarity** agar perbandingan mencerminkan kualitas representasi intrinsik, bukan perbedaan algoritma retrieval.

Seluruh eksperimen utama menggunakan **frozen representations** (tanpa *fine-tuning*).

## 5. Dataset dan perannya (Pembaruan DEC-09 / Gate 1-R)

Sesuai audit 12 September 2026 (**DEC-09**), korpus eksperimen utama dialihkan ke **BirdCLEF+ 2026** guna menjamin kecukupan daya statistik (\(n=200\) kueri bersih) dan integritas data bebas bocor:

### Galeri dan Kueri Bersih: BirdCLEF+ 2026
- **Spesies Target**: 20 spesies burung terkurasi ketat (§11.3: koleksi Xeno-Canto, Aves, rating \(\ge 3.0\), klip \(\ge 20\), perekam \(\ge 3\)). Dari 156 kandidat lolos ambang, 20 spesies dipilih berdasarkan diversitas perekam tertinggi (\(n_{\text{author}}\)), sedangkan 136 tersisih murni akibat kuota 20 taksa (DEC-10).
- **Total Korpus Aktif**: 4.351 berkas rekaman audio.
- **Standar Prapemrosesan**: Durasi 5,0 detik (160.000 sampel), laju sampel 32 kHz, mono, normalisasi energi RMS = 0.05.
### Bank Derau Aditif (E2) & Negatif Open-Set (E3): Rekaman AudioMoth ITERA
- Perekaman nyata *ambient soundscape* kampus ITERA (Embung, Hutan Mini/Arboretum, dan area antropogenik) menggunakan perangkat **AudioMoth**.
- **Derau sintetis (pink noise) resmi ditinggalkan** per DEC-09 karena tidak memiliki validitas ekologis untuk bioakustik tropis.
- Folder `data/itera_noise/` diisi rekaman berdurasi 5 detik tanpa suara burung target untuk eksperimen E2 (pencampuran SNR terkontrol) dan E3 (penolakan open-set).

### Real Soundscape Validation (E4)
- Menggunakan subset teranotasi dari `train_soundscapes` BirdCLEF+ 2026 untuk mengukur kesenjangan (*gap*) antara derau terkontrol dan pergeseran domain nyata.

## 6. Split penelitian (Strict Recordist-Disjoint)

Partisi data dibekukan di `data/manifests/dataset_split.csv` menggunakan pembagian identitas perekam mutlak (*Strict Global Recordist-Disjoint*, `seed=42`):

```text
BirdCLEF+ 2026 (4.351 klip | 20 spesies)
├── gallery      : 3.653 klip (377 perekam unik) -> Koleksi referensi pencarian
├── query_clean  :   200 klip ( 68 perekam unik) -> 10 kueri bersih per spesies
└── calibration  :   498 klip ( 95 perekam unik) -> Kalibrasi ambang jarak open-set
```

Jaminan integritas matematis:
- **Zero Recordist Overlap**: 0 perekam beririsan antar galeri, kueri, dan kalibrasi.
- **Zero Recording ID Overlap**: 0 rekaman muncul lebih dari satu peran.
- **Zero Filepath Overlap**: 0 duplikasi berkas fisik.
- Diverifikasi otomatis oleh `tests/test_split_leakage.py` dan `tests/integration/test_split_leakage.py`.

## 7. Controlled noise experiment

Setiap clean query dibuat menjadi beberapa versi menggunakan noise ITERA yang sama dan seed yang dibekukan.

Rancangan awal:

```text
clean
20 dB
10 dB
0 dB
-5 dB
```

Level final boleh disesuaikan saat pilot untuk menghindari seluruh model mengalami ceiling/floor effect. Setelah pilot, level SNR dibekukan.

Untuk setiap representasi:

```text
query audio
   ↓
representation extraction
   ↓
embedding
   ↓
cosine similarity terhadap gallery
   ↓
ranking
   ↓
mAP@k / Recall@k / Precision@k
```

## 8. Open-set experiment

Query open-set meliputi:

- unknown bird species yang tidak ada dalam gallery target;
- background-only ITERA;
- non-bird environmental events bila tersedia.

Sistem menerima match bila:

```text
max_similarity(query, gallery) >= threshold
```

Threshold dipilih hanya dari calibration split dan kemudian **dibekukan**.

## 9. Metrik evaluasi

### Retrieval primer

- `mAP@k`
- `Recall@1`
- `Recall@5`
- `Recall@10`
- `Precision@k`

### Robustness

- raw `mAP@k` per SNR;
- absolute performance drop;
- relative robustness retention;
- kurva `metric vs SNR`.

### Open-set

- AUPRC;
- AUROC;
- F1 pada threshold calibration;
- false-positive / false-accept rate;
- recall/TPR pada operating point.

### Sekunder

- median rank / MRR bila berguna;
- embedding dimension;
- inference time;
- UMAP/t-SNE hanya untuk visualisasi, bukan success criterion.

## 10. Rencana eksperimen dan Status Eksekusi

### E0 — Pipeline Sanity Check (Status: SELESAI & LULUS 100%)
- **Notebook**: `notebooks/E0_Pipeline_Sanity_Check.ipynb`
- Partisi data *Strict Global Recordist-Disjoint* (`seed=42`) lolos uji kebocoran 100% (*zero leakage assertion gate* aktif).
- *Smoke test* ekstraksi fitur R0, R1, R2, R3 pada audio riil `XC1053050.ogg` terverifikasi presisi dimensi, bernorma L2 unit, dan bebas `NaN`/`Inf`.
- Uji hipotesis kontrol negatif H5 terbukti valid: model terlatih secara signifikan mengungguli tebakan acak (\(R2=85.0\% > R1=40.0\% > R0=5.0\% \gg R3=10.0\%\)).

### E1 — Clean Retrieval Benchmark (Status: SELESAI & LULUS 100%)
- **Notebook**: `notebooks/E1_Clean_Retrieval.ipynb`
- Menguji 200 kueri bersih terhadap 3.653 rekaman galeri lintas 20 spesies burung target.
- Hasil evaluasi kanonikal tersimpan di `results/processed/clean_retrieval_table.csv` dan `paper/tables/clean_retrieval_table.csv`:

| Representasi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **R0: MFCC Baseline (40-d)** | 27.5% | 0.1319 | 0.4224 | 0.2175 | 0.0123 |
| **R1: PANNs CNN14 (2048-d)** | 60.0% | 0.4152 | 0.7005 | 0.5025 | 0.0291 |
| **R2: BirdNET Backbone (1024-d)** | **95.0%** | **0.9126** | **0.9658** | **0.9280** | **0.0528** |
| **R3: Random Control (40-d)** | 6.5% | 0.0190 | 0.1779 | 0.0530 | 0.0028 |

- Rekaman per-kueri (*query-level log*) lengkap tersimpan di `results/processed/per_query_clean_retrieval.csv` (memuat `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, dan `AP@10` per rekaman).
- Visualisasi metrik tersimpan di `results/figures/clean_retrieval_benchmark.png` dan `paper/figures/clean_retrieval_benchmark.png`.

### E2 — Controlled Noise Robustness (Jadwal: Minggu 2 / H8–H14)
- 200 kueri bersih dipasangkan secara deterministik dengan rekaman derau AudioMoth ITERA pada 4 tingkat SNR: +20 dB, +10 dB, 0 dB, dan -5 dB.
- Mengukur kurva degradasi performa (*relative robustness retention*) untuk seluruh representasi.

### E3 — Open-Set Threshold (Jadwal: Minggu 3 / H15–H21)
- Penentuan ambang kemiripan \(\tau\) dari 498 klip set kalibrasi menggunakan Youden's J pada target FAR 5% dan 10%.
- Pengujian transfer ambang beku terhadap unknown mirip (burung non-target), unknown non-burung, dan derau murni ITERA.

### E4 — Real Soundscape Domain Shift (Jadwal: Minggu 3 / H18)
- Evaluasi pipeline beku pada rekaman bentang suara nyata (`train_soundscapes` BirdCLEF) tanpa *re-tuning* ambang.

### E5 — Failure Case Analysis (Jadwal: Minggu 3 / H19–H20)
- Audit mendalam minimal 20 kasus salah temu (*false accept* dan *false reject*) yang dianalisis secara manual per kueri.

### E6 — External Public Validation (Opsional)
- Pengujian generalisasi eksternal setelah E0–E5 tuntas.

## 11. Struktur repository (Status Aktif Pasca-Pembersihan)

```text
DSIC-2706/
├── README.md                                          # Dokumentasi utama dan roadmap lab
├── pyproject.toml / requirements.txt                  # Dependensi lingkungan Python
├── run_tests.py                                       # Suite uji saintifik otomatis (9/9 lulus)
│
├── data/
│   ├── manifests/
│   │   ├── dataset_split.csv                          # Manifes kanonik 4.351 klip (Recordist-Disjoint)
│   │   ├── species_freeze.csv                         # 20 spesies target resmi (DEC-10)
│   │   ├── species_excluded.csv                       # Transparansi eliminasi 186 taksa
│   │   └── itera_noise_manifest.csv                   # Manifes bank derau AudioMoth ITERA
│   ├── BirdClef/                                      # Data primer BirdCLEF+ 2026
│   ├── itera_noise/                                   # Wadah rekaman soundscape AudioMoth ITERA
│   └── xeno_canto/                                    # Aset arsip rekaman mentah Xeno-Canto
│
├── notebooks/                                         # 4 Notebook Resmi Gate 1-R
│   ├── EDA_Tugas_Akhir.ipynb                          # Eksplorasi dataset & inventarisasi
│   ├── Preprocessing Verification.ipynb               # Validasi pemotongan & normalisasi RMS
│   ├── E0_Pipeline_Sanity_Check.ipynb                 # Verifikasi anti-kebocoran & smoke test
│   └── E1_Clean_Retrieval.ipynb                       # Tolok ukur retrieval kueri bersih
│
├── src/                                               # Modul pemrosesan terpusat
│   ├── preprocess.py                                  # Audio pipeline (32 kHz, 5s, RMS 0.05)
│   ├── embeddings.py                                  # Ekstraktor representasi (R0, R1, R2, R3)
│   ├── mix_noise.py                                   # Engine pencampuran SNR terkontrol
│   └── evaluate.py                                    # Komputasi metrik Information Retrieval
│
├── tests/                                             # Suite pengujian saintifik
│   ├── test_split_leakage.py                          # Verifikasi matematis zero leakage
│   ├── test_snr_mixing.py                             # Verifikasi akurasi rumus SNR
│   ├── test_cosine.py                                 # Verifikasi batas kesamaan kosinus
│   ├── test_threshold_freeze.py                      # Verifikasi stabilitas ambang beku
│   ├── unit/                                          # Uji integritas manifes SHA-256 & model
│   └── integration/                                   # Uji integrasi kebocoran partisi
│
├── results/
│   ├── features/                                      # Cache embedding NPZ (R0, R1, R2, R3)
│   ├── processed/                                     # Tabel hasil evaluasi kanonikal
│   ├── figures/                                       # Grafik saintifik E1
│   └── archive/                                       # Arsip aman hasil & skrip lama
│       └── 2026-09-07_xenocanto16spesies/             # Arsip eksperimen 14-spesies Gate 1
│
├── paper/
│   ├── figures/                                       # Gambar resolusi tinggi untuk naskah
│   └── tables/                                        # Tabel metrik tersinkronisasi
│
├── docs/research/
│   ├── decision-log.md                                # Catatan keputusan resmi (DEC-01 s.d DEC-10)
│   └── scope-freeze.md                                # Pembekuan cakupan versi 3.0
│
└── Rencana-eksperimen-bimbingan/
    └── CATATAN_PROGRES_BIMBINGAN.md                   # Log mingguan bimbingan TA
```

## 12. Tools

Minimum stack:

- Python 3.11/3.12;
- librosa;
- soundfile;
- scipy;
- NumPy;
- pandas;
- scikit-learn;
- PyTorch/TensorFlow sesuai pretrained checkpoint;
- matplotlib;
- FAISS opsional;
- UMAP opsional;
- Git.

Untuk audio lapangan:

- AudioMoth / field recorder bila tersedia;
- WAV lebih disarankan;
- konfigurasi recorder, lokasi, daypart, dan timestamp dicatat.

## 13. Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Salin konfigurasi:

```bash
cp .env.example .env
```

Validasi repository:

```bash
make test
```

Pipeline awal:

```bash
make manifest
make sanity
make clean-retrieval
```

Eksperimen utama:

```bash
make noise-robustness
make open-set
make soundscape
make evaluate
make figures
```

Perintah pada Makefile adalah skeleton dan harus dihubungkan ke implementasi final.

## 14. Aturan reproducibility

Setiap run minimal menyimpan:

```text
run_id
representation
checkpoint/version
query_id
gallery_manifest_version
noise_id
SNR
random_seed
threshold_version
ranking
metrics
runtime
```

Setiap klaim artikel harus dapat ditelusuri:

```text
RQ
 ↓
experiment
 ↓
raw result
 ↓
processed result
 ↓
table / figure
 ↓
claim
```

## 15. Data dan Git

Jangan commit file WAV besar ke repository.

Yang boleh di-version-control:

- manifest;
- metadata;
- checksum;
- annotation;
- configuration;
- code;
- result summary.

Yang tidak di-commit:

- raw audio besar;
- pretrained weights besar;
- temporary embedding cache;
- generated experiment artifacts besar.

## 16. Rencana satu bulan

### Minggu 1

- target species freeze;
- manifest Xeno-Canto;
- recording/preprocessing protocol;
- MFCC + dua embedding smoke test;
- clean retrieval baseline.

### Minggu 2

- ITERA noise bank;
- SNR mixer;
- E1/E2 main run;
- robustness curves.

### Minggu 3

- unknown/background set;
- threshold calibration;
- open-set test;
- annotated ITERA soundscape subset;
- failure audit.

### Minggu 4

- paired bootstrap CI;
- final tables/figures;
- domain-shift analysis;
- manuscript draft;
- fresh reproducibility run.

Untuk skripsi empat bulan, bulan berikutnya dapat digunakan untuk memperbesar data, menambah seed/recordist-disjoint checks, external validation, dan pematangan artikel tanpa mengubah RQ utama.

## 17. Definition of Done

Penelitian utama dianggap selesai bila:

- [ ] target taxon dan species list dibekukan;
- [ ] split bebas duplicate leakage;
- [ ] MFCC baseline selesai;
- [ ] generic pretrained representation selesai;
- [ ] satu bioacoustic representation selesai;
- [ ] clean retrieval selesai;
- [ ] minimal tiga noisy conditions selesai;
- [ ] `mAP@k` dan `Recall@k` dihitung;
- [ ] threshold berasal hanya dari calibration;
- [ ] open-set metrics tersedia;
- [ ] real soundscape external check selesai;
- [ ] minimal 20 failure cases diaudit;
- [ ] confidence interval tersedia;
- [ ] data manifest, seed, config, dan version model terdokumentasi;
- [ ] satu tabel dan satu figure dapat direproduksi dari fresh run;
- [ ] tidak ada klaim kehadiran spesies tanpa verifikasi manual.

## 18. Publication boundary

Paper utama menjawab **robustness of representation for retrieval**.

Luaran aplikasi seperti candidate biodiversity observations di ITERA hanya merupakan secondary output. Jangan mengubah paper menjadi ecological inventory study tanpa RQ, sampling design, dan ground truth ekologis yang baru.

## Catatan Pembimbing

Alur besarnya kira-kira seperti ini:

```text
Xeno-Canto
   ↓
pilih 10–20 spesies burung
   ↓
bersihkan + segmentasi audio
   ↓
pisahkan
Gallery | Query | Calibration | Test
   ↓
ekstrak representasi
MFCC | Generic Embedding | Bioacoustic Embedding
   ↓
Cosine Similarity
   ↓
Ranking audio paling mirip
   ↓
Clean retrieval
   ↓
tambahkan noise ITERA pada query yang SAMA
   ↓
20 dB → 10 dB → 0 dB → -5 dB
   ↓
ukur penurunan retrieval
   ↓
open-set threshold
   ↓
uji pada real soundscape ITERA
```

Secara eksperimen bisa seperti berikut.

1. **Mulai dari membuat “bank referensi” burung, bukan langsung merekam ITERA.** Mahasiswa memilih sekitar 10–20 spesies target terlebih dahulu. Audio referensinya dikumpulkan dari Xeno-Canto, kemudian dibuat manifest yang menyimpan spesies, recording ID, recordist, lokasi, lisensi, dan attribution. Audio kemudian distandardisasi: sample rate, durasi potongan, mono/stereo, dan normalisasi harus sama. Xeno-Canto kemudian dipisah menjadi **gallery** dan **query**; rekaman yang sama tidak boleh bocor ke kedua sisi. Pada minggu pertama audit juga mensyaratkan manifest, preprocessing, split, dan clean baseline sudah selesai. 

   Misalnya ada suara burung A. Beberapa rekamannya masuk ke gallery sebagai “koleksi yang dicari”, sedangkan rekaman burung A yang berbeda menjadi query. Jadi sistem diberi satu query dan ditanya: **dari seluruh gallery, audio mana yang paling mirip?**

2. **Setiap audio diubah menjadi tiga bentuk representasi.** Representasi pertama adalah baseline klasik **MFCC**. Representasi kedua adalah *generic pretrained audio embedding*, misalnya PANNs. Representasi ketiga adalah satu model yang memang lebih khusus bioakustik. Semua dipakai sebagai **feature extractor**, bukan dilatih ulang pada test data. Kemudian ketiganya menggunakan similarity metric yang sama, yaitu cosine similarity. Ini penting supaya yang dibandingkan benar-benar kualitas representasinya, bukan karena satu metode memakai retrieval algorithm yang berbeda. Baseline dan kontrol di audit adalah MFCC + cosine, random ranking, generic deep embedding + cosine, dan bioacoustic embedding + cosine. 

   Jadi untuk satu audio:

```text
audio.wav
   ├── MFCC                 → vector A
   ├── PANNs embedding      → vector B
   └── bioacoustic embedding → vector C
```

Lalu untuk masing-masing ruang vektor dilakukan:

```text
cosine(query, gallery_1)
cosine(query, gallery_2)
...
cosine(query, gallery_n)
```

Hasilnya diurutkan dari similarity tertinggi sampai terendah.

3. **Eksperimen pertama justru dilakukan dalam kondisi bersih.** Ini E1. Gallery tidak berubah dan query bersih benar-benar berbeda dari gallery. Lalu dihitung mAP@k, Recall@1, Recall@5, Recall@10, dan Precision@k.  Tujuannya bukan mencari novelty dahulu, tetapi memastikan pipeline masuk akal. Kalau random ranking ternyata sama bagusnya dengan embedding, berarti ada masalah pada label, split, atau implementasi similarity.

   Misalnya query “spesies A”. Jika lima hasil teratas adalah:

```text
1. A
2. A
3. B
4. A
5. C
```

dari sini kita bisa menghitung Precision@5, Recall@5, AP, dan seterusnya.

4. **Baru di sini eksperimen utama DSIC27-06 dimulai: query yang sama diberi noise ITERA.** Mahasiswa merekam **background-only** di ITERA—misalnya area Embung, Arboretum/Kebun Raya, dan area yang lebih antropogenik. Noise tersebut tidak boleh mengandung vocalization target yang kuat. Lalu clean query dari tahap sebelumnya dicampur dengan noise yang sama secara terkontrol. Audit menggunakan kondisi clean, 20 dB, 10 dB, 0 dB, dan -5 dB sebagai rancangan awal. 

   Jadi query Q yang sama menjadi:

```text
Q_clean
Q_20dB
Q_10dB
Q_0dB
Q_-5dB
```

Lalu kelima versi itu masuk ke **MFCC, generic embedding, dan bioacoustic embedding yang sama**.

Inilah yang membuat eksperimennya kuat. Kita tidak membandingkan audio berbeda pada tiap kondisi. Kita membandingkan **paired query**:

```text
burung yang sama
rekaman yang sama
gallery yang sama
hanya noise level yang berubah
```

Dari situ akan terbentuk kurva seperti:

```text
mAP@k
  |
  |\
  | \      Bioacoustic embedding
  |  \
  |   \    Generic embedding
  |    \
  |     \  MFCC
  +---------------- SNR
   clean 20 10 0 -5
```

Pertanyaan ilmiahnya menjadi sangat jelas: **siapa yang turun paling lambat?**

5. **Setelah retrieval robustness, baru lakukan open-set experiment.** Soundscape nyata tidak selalu berisi salah satu spesies yang ada di gallery. Karena itu kita butuh kemampuan sistem untuk berkata **“tidak ada kecocokan yang cukup meyakinkan.”** Dibuat calibration set yang berisi known dan unknown. Dari calibration set itu dipilih threshold similarity \(\tau\). Setelah \(\tau\) ditetapkan, nilainya **dibekukan** dan tidak boleh disetel lagi menggunakan test set. Audit secara eksplisit meminta pemisahan calibration known/unknown dan test known/unknown, lalu mengukur F1, AUROC, AUPRC, FPR/FAR, dan recall setelah threshold dibekukan. 

   Logikanya sederhana:

```text
max_similarity >= τ  → accept candidate species
max_similarity <  τ  → reject / unknown
```

Yang menarik secara penelitian bukan hanya mencari \(\tau\) terbaik. Yang kita uji adalah:

**threshold yang dipilih saat calibration itu masih bekerja tidak ketika noise bertambah?**

Misalnya \(\tau=0.72\) bagus pada clean audio, tetapi ketika 0 dB hampir semua unknown ikut diterima. Itu adalah hasil ilmiah yang penting.

6. **Terakhir barulah masuk real soundscape ITERA.** Ini berbeda dengan eksperimen noise sintetis. Pada controlled mixing, kita tahu persis ground truth-nya karena vocalization berasal dari query Xeno-Canto yang diketahui. Pada real soundscape, masalahnya jauh lebih sulit: jarak mikrofon berubah, reverberasi, suara kendaraan, overlap beberapa burung, arah sumber, respons mikrofon, dan lain-lain terjadi bersamaan. Karena itu audit memisahkan **controlled noise** dan **real domain shift**. Frozen pipeline dijalankan pada subset soundscape ITERA yang sudah dianotasi, dan threshold tidak boleh di-*retune* menggunakan label test ITERA. 

   Jadi hasil akhir yang menarik bukan:

   > “BirdNET menemukan 25 spesies di ITERA.”

   tetapi:

   > “Representasi bioakustik mempertahankan retrieval lebih baik sampai SNR tertentu, tetapi terjadi gap sebesar X ketika berpindah dari controlled noise ke real ITERA soundscape.”

   Itu jauh lebih kuat sebagai penelitian.

7. **Sesudah itu dilakukan failure analysis.** Kita ambil false positive dan false negative paling menarik, lalu diperiksa penyebabnya: suara tumpang tindih, noise antropogenik, SNR rendah, dua spesies dengan vocalization mirip, jarak jauh/reverberasi, event terlalu pendek, atau background signature. Audit meminta minimal failure cases yang dibahas, bukan hanya satu tabel metrik. 

Untuk tools-nya sebenarnya tidak berat. **Python** menjadi pusat pipeline. `librosa`, `soundfile`, `scipy`, dan bila perlu `ffmpeg` dipakai untuk audio preprocessing dan mixing. Untuk deep embedding digunakan **PyTorch atau TensorFlow** sesuai checkpoint, dengan PANNs sebagai generic representation dan satu implementasi bioacoustic embedding. Similarity retrieval cukup dengan **NumPy/scikit-learn**; FAISS baru diperlukan kalau gallery sudah besar. Statistik memakai `pandas`, `NumPy`, `scipy`, dan bila perlu `statsmodels` atau bootstrap sendiri. Visualisasi cukup `matplotlib`; UMAP hanya pendukung. Untuk reproducibility digunakan Git, YAML config, seed, manifest, checksums, dan lock file. Rekaman ITERA dapat memakai field recorder atau **AudioMoth bila tersedia**, dengan konfigurasi perekam dicatat. 

Jadi **tidak perlu Spark, Hadoop, training GPU besar, database kompleks, atau membuat aplikasi mobile** untuk menjawab RQ ini. GPU akan membantu mempercepat ekstraksi pretrained embedding, tetapi setelah embedding tersimpan, cosine retrieval-nya ringan.

Yang paling penting: penelitian ini bukan pertanyaan **“model mana paling akurat?”**, tetapi pertanyaan **“ketika lingkungan makin buruk, representation mana yang kehilangan kemampuan similarity retrieval paling lambat, dan apakah keputusan accept/reject-nya tetap stabil ketika pindah ke kondisi lapangan nyata?”** begitulah inti eksperimennya.

---

## 8. Daftar Periksa H1
* **Kepatuhan:**
  - [x] Aturan kompetisi dibaca dan disetujui
  - [x] Klausul penggunaan akademik disalin ke `docs/protocols/birdclef-license.md` beserta URL dan tanggal akses
  - [x] Pertanyaan D-07 diajukan ke Supervisor 1 (Disetujui/Diarahkan langsung oleh Supervisor 1)
* **Unduhan:**
  - [x] Ruang disk diperiksa sebelum mengunduh
  - [x] Data terunduh dan diekstrak
  - [x] `data/birdclef2026/` masuk `.gitignore`
  - [x] Lima berkas audio diuji baca (FLAC/OGG) — pada H1, bukan H4
* **Inventaris:**
  - [x] `scripts/inventory_birdclef.py` ditulis dan dijalankan
  - [x] `data/manifests/birdclef_inventory.json` dihasilkan
  - [x] Sepuluh butir §1.2 seluruhnya terjawab
  - [x] Tidak ada angka dataset yang diketik tangan ke dokumen mana pun
* **Keputusan:**
  - [x] Kelayakan dataset dinilai (§3.1)
  - [x] Laju sampel analisis ditetapkan dan dibekukan (§3.2)
  - [x] Kelayakan E4 dinilai (§3.3)
  - [x] Penanganan Unknown diputuskan (§3.4)

---

## BAGIAN V — TEKNIS LAB MINGGU 2–4
Bagian ini melengkapi Bagian II yang hanya mencakup Minggu 1. Penomoran hari mengikuti Rencana Kerja 1 Bulan pada §19: Minggu 2 adalah H8–H14, Minggu 3 adalah H15–H21, dan Minggu 4 adalah H22–H30. Setiap minggu ditutup satu gate yang harus diverifikasi Supervisor 1 sebelum minggu berikutnya dimulai.
Prinsip yang berlaku di seluruh bagian ini sama dengan Bagian II: setiap pemeriksaan mutu ditulis sebagai gerbang yang menggagalkan eksekusi, bukan sebagai baris laporan yang hanya dicetak.

### MINGGU 2 (H8–H14) — E2 Controlled Noise Robustness

#### H8 — Bekukan mesin pencampuran SNR
Empat pekerjaan, seluruhnya prasyarat sebelum satu pun angka dihasilkan:
1. Hapus jalur cadangan pink noise pada `src/mix_noise.py` dan ubah menjadi melempar galat bila bank derau kosong. Selama jalur itu hidup, eksperimen dapat berjalan memakai derau sintetis tanpa ada yang menyadarinya — persis penyebab temuan M-05 tidak terdeteksi selama dua audit.
2. Implementasikan pemasangan query ke segmen derau secara deterministik dengan seed tetap, lalu simpan pemasangannya sebagai manifes. Pemasangan acak tanpa catatan membuat hasil tidak dapat direproduksi.
3. Sebarkan tipe lokasi derau merata pada setiap tingkat SNR. Bila query pada 0 dB kebetulan mendapat derau antropogenik sedangkan pada 10 dB mendapat ambien vegetasi, perbedaan performa akan bercampur perbedaan jenis derau.
4. Tambahkan uji unit yang memverifikasi SNR terukur pada sinyal hasil pencampuran sesuai target dalam toleransi yang ditetapkan, misalnya ±0,5 dB.
Jalankan pula kontrol B6 no-op audio transform dari §13: lakukan resample dan write-read tanpa menambah derau, lalu tunjukkan bahwa prapemrosesan itu sendiri tidak menyebabkan penurunan mAP yang berarti. Kontrol ini menjadi penting karena derau AudioMoth diturunkan lajunya ke laju analisis sementara audio BirdCLEF mungkin tidak.

#### H9 — Pilot tingkat SNR, lalu bekukan gridnya
Jalankan subset kecil, misalnya 3 spesies × 5 query × seluruh representasi, pada grid SNR kandidat. Tujuannya satu: memastikan grid tidak mengalami ceiling maupun floor total.
- jika seluruh representasi masih hampir sempurna pada −5 dB -> grid terlalu ringan, tambahkan kondisi lebih berat
- jika seluruh representasi kolaps sudah pada 0 dB -> grid terlalu berat, geser ke atas
- jika R3 acak tidak jauh di bawah R0/R1/R2 -> pipeline atau metrik bermasalah, hentikan
Setelah pilot, grid SNR dibekukan dan dicatat pada decision-log sebagai keputusan bernomor. Grid tidak boleh diubah lagi setelah main run dimulai, dan tidak boleh dipilih setelah melihat representasi mana yang menang. Ini syarat §16 butir 6 dan merupakan pembeda antara eksperimen terkontrol dan penyesuaian post-hoc.

#### H10 — Bekukan segmen derau dan seed
Manifes pemasangan query ke segmen derau dibekukan dan di-checksum. Verifikasi bahwa menjalankan ulang dari seed yang sama menghasilkan pemasangan yang identik.

#### H11–H12 — Jalankan E1 dan E2 untuk seluruh query
Jalankan seluruh kombinasi representasi × kondisi SNR. Dua hal yang wajib disimpan dan sering terlupakan:
1. Ranking per query, bukan hanya metrik agregat. Tanpa ini, analisis kegagalan pada Minggu 3 tidak mungkin dilakukan dan auditor tidak dapat memeriksa ulang apa pun.
2. Catatan eksekusi di samping setiap tabel: waktu, SHA Git, konfigurasi efektif, dimensi embedding aktual, versi pustaka, dan run_id.
Simpan pula run yang gagal, jangan dibuang. Run gagal adalah data untuk analisis kegagalan, bukan sampah.

#### H13 — Kurva ketahanan awal
Hasilkan mAP@10 terhadap SNR, Recall@k terhadap SNR, dan relative retention terhadap SNR untuk setiap representasi.
Laporkan skor mentah berdampingan dengan retensi relatif, tidak hanya rasionya. Representasi dengan skor bersih rendah dapat tampak stabil secara semu. Audit sebelumnya menemukan kontrol acak R3 mencapai retensi 1,409 pada 10 dB — itu artefak aritmetika ketika penyebut mendekati nol, bukan temuan, dan wajib diberi catatan kaki.

#### H14 — Buffer dan verifikasi Gate 2
Hari ini sengaja dikosongkan sebagai penyangga. Bila H8–H13 berjalan lancar, pakai untuk analisis sekunder tipe derau: bandingkan mAP@10 pada SNR yang sama menurut derau perairan, vegetasi, dan antropogenik. Datanya sudah ada sehingga biayanya hampir nol.

#### Gate 2 — daftar periksa kelulusan
- [ ] Jalur cadangan pink noise dihapus; bank derau kosong menyebabkan galat, bukan derau sintetis.
- [ ] Grid SNR dibekukan setelah pilot dan tercatat di decision-log sebelum main run.
- [ ] Tidak ada ceiling maupun floor total pada grid beku.
- [ ] Kontrol acak R3 jauh di bawah R0, R1, dan R2 pada seluruh kondisi.
- [ ] Pasangan query konsisten: query yang sama muncul pada seluruh kondisi SNR.
- [ ] Ranking per query tersimpan untuk seluruh kombinasi representasi × kondisi.
- [ ] Pemasangan query↔segmen derau deterministik dan dapat direproduksi dari seed.
- [ ] Tipe lokasi derau tersebar merata pada setiap tingkat SNR.
- [ ] Kontrol B6 no-op lulus.
- [ ] Skor mentah dan retensi relatif sama-sama dilaporkan.
- [ ] Catatan eksekusi menyertai setiap tabel hasil.

### MINGGU 3 (H15–H21) — E3 Open-Set, E4 Domain Shift, E5 Failure Analysis

#### H15 — Susun tiga jenis unknown, dengan pembagian terstratifikasi
Himpunan unknown terdiri atas tiga jenis yang harus dipisahkan sejak awal dan dilaporkan terpisah sampai akhir:
| Jenis | Isi | Menguji |
|---|---|---|
| (a) Unknown mirip | Spesies burung BirdCLEF yang tidak ada di gallery | Penolakan terhadap unknown yang mirip secara biologis |
| (b) Unknown non-burung | Takson non-burung BirdCLEF: amfibi, reptil, mamalia, serangga | Penolakan terhadap satwa lain pada bentang suara yang sama |
| (c) Derau murni | Segmen background-only ITERA | Penolakan terhadap kondisi tanpa satwa target sama sekali |

Pembagian kalibrasi dan uji wajib terstratifikasi menurut takson dengan seed tetap. Audit sebelumnya menemukan pembagian dilakukan dengan potongan posisional sehingga proporsi mamalia bergeser dari 42,5 persen saat kalibrasi menjadi 17,9 persen saat pengujian — dan ketidakstabilan ambang menjadi bercampur dengan pergeseran komposisi takson. Proporsi takson pada kedua sisi dicatat di manifes.
Pastikan pula unknown yang dipakai untuk kalibrasi tidak dipakai lagi sebagai unknown uji.

#### H16 — Kalibrasi dan pembekuan ambang τ
Pilih τ dari calibration split saja, memakai Youden's J sesuai DEC-04. Setelah dipilih, τ dicatat nilainya, di-commit, dan tidak boleh disentuh lagi. Test set tidak boleh dipakai untuk mencari τ dalam keadaan apa pun.
Tambahkan gerbang: skrip evaluasi menolak berjalan bila nilai τ yang dipakai berbeda dari nilai yang tercatat pada berkas beku.

#### H17 — Uji transfer ambang lintas SNR
Jalankan τ beku pada kondisi bersih dan seluruh tingkat SNR. Laporkan AUPRC, AUROC, F1 pada τ, FPR/FAR, dan recall pada titik operasi — masing-masing terpisah untuk unknown jenis (a), (b), dan (c).
Perhatikan bahwa kestabilan ambang punya dua sisi yang dapat berlawanan arah. Audit sebelumnya menemukan R2 paling stabil pada sisi FPR namun justru paling dalam penurunannya pada sisi recall. Keduanya harus dilaporkan, dan kesimpulan tidak boleh digeneralkan dari satu sisi saja.

#### H18 — E4 pergeseran domain nyata
Jalankan pipeline beku pada train_soundscapes BirdCLEF. Tiga larangan yang mengikat:
1. Jangan mengkalibrasi ulang τ memakai label soundscape.
2. Jangan mengubah representasi, gallery, atau prapemrosesan.
3. Jangan memakai test_soundscapes — labelnya tersembunyi dan tidak berguna di sini.
Laporkan selisih antara campuran terkontrol dan soundscape nyata pada tingkat SNR yang sebanding. Selisih inilah yang menjawab H3, dan wajib dilaporkan terpisah dari E2 karena pergeseran domain nyata mencakup jarak, reverberasi, respons mikrofon, dan tumpang tindih panggilan sekaligus — bukan sekadar penjumlahan derau.

#### H19–H20 — E5 analisis kegagalan
Audit minimal 20 kasus kegagalan, mencakup false positive dan false negative. Kelompokkan penyebabnya menurut kategori §14: tumpang tindih panggilan, derau antropogenik, SNR rendah, vokalisasi spesies mirip, jarak dan reverberasi, event pendek, serta sidik jari latar.
Diagnosis wajib ditulis manusia setelah mendengarkan kasusnya. Audit sebelumnya menemukan kolom diagnosis berisi satu kalimat template yang hanya berganti nama spesies; tabel semacam itu tidak memenuhi syarat analisis kegagalan meskipun query_id dan skornya nyata.

#### H21 — Buffer dan verifikasi Gate 3
Penyangga untuk pekerjaan yang meleset. Bila lancar, pakai untuk menyiapkan distribusi skor kemiripan known versus unknown dan kurva precision-recall open-set yang menjadi butir wajib §18.

#### Gate 3 — daftar periksa kelulusan
- [ ] Tiga jenis unknown disusun terpisah dan dilaporkan terpisah.
- [ ] Pembagian kalibrasi/uji terstratifikasi menurut takson; proporsinya tercatat.
- [ ] Unknown kalibrasi tidak dipakai ulang sebagai unknown uji.
- [ ] τ dipilih hanya dari calibration, dibekukan, dan di-commit sebelum menyentuh test.
- [ ] Skrip menolak berjalan bila τ menyimpang dari nilai beku.
- [ ] AUPRC, AUROC, F1@τ, FPR/FAR tersedia untuk seluruh kondisi SNR.
- [ ] Sisi FPR dan sisi recall dilaporkan terpisah, tanpa generalisasi.
- [ ] E4 dijalankan tanpa kalibrasi ulang dan tanpa test_soundscapes.
- [ ] Selisih campuran terkontrol versus soundscape nyata dilaporkan.
- [ ] Minimal 20 kasus kegagalan diaudit dengan diagnosis yang ditulis manusia.
- [ ] Tidak ada diagnosis template yang berulang.

### MINGGU 4 (H22–H30) — Statistik, Penulisan, Reproduksi

#### H22–H23 — Statistik berpasangan
Ini penutup temuan M-03 yang terbuka sejak audit pertama. Bootstrap yang ada sebelumnya me-resample tiap kondisi secara terpisah; yang disyaratkan adalah bootstrap berpasangan atas selisih per query.
```python
untuk b = 1..1000:
    ambil ulang INDEKS QUERY dengan pengembalian
    d_b = rata-rata( AP_R2[idx] - AP_R1[idx] )
CI 95% = persentil 2,5 dan 97,5 dari {d_b}
selisih terdukung bila CI tidak memuat nol
```
Unit resampling adalah query atau rekaman, bukan tiap salinan berderau; salinan berderau dari query yang sama bukan sampel independen penuh. Terapkan koreksi Holm untuk banyak perbandingan berpasangan antar representasi dan antar SNR. Interval kepercayaan dimasukkan ke tabel dan ditampilkan sebagai pita atau batang galat pada gambar.
Analisis utama ditetapkan sebelum melihat hasil uji penuh. Ambang efek minimum yang dianggap bermakna secara praktis juga ditetapkan di muka, bukan setelah melihat angka.
Perlu diantisipasi bahwa sebagian selisih mungkin memiliki CI yang memuat nol. Bila itu terjadi, hasilnya tetap dilaporkan apa adanya. Hasil nol atau MFCC yang kompetitif tetap bernilai ilmiah bila eksperimennya terkontrol, dan §17 menegaskan penelitian dinilai dari validitas protokol, bukan dari kemenangan deep embedding.

#### H24 — Gambar dan tabel wajib
Gunakan daftar 11 butir pada §18 sebagai daftar periksa, bukan sebagai saran. Setiap butir yang tidak dibuat harus punya alasan tertulis.

#### H25–H26 — Penulisan
Tulis Metode, Hasil, dan Threats to Validity. Empat hal yang wajib muncul dan mudah terlewat:
1. Hapus kata “signifikan” dari abstrak dan pembahasan kecuali didukung CI berpasangan yang tidak memuat nol.
2. Bahas kontaminasi pralatih secara eksplisit: BirdNET dilatih pada Xeno-Canto sedangkan train_audio BirdCLEF bersumber dari Xeno-Canto dan iNaturalist. Ini syarat quality gate artikel pada §25.
3. Nyatakan ketidakcocokan geografis: spesies Pantanal, derau Sumatera. Derau diperlakukan sebagai gangguan akustik terkendali, bukan skenario ekologis.
4. Nyatakan sidik jari AudioMoth: seluruh derau berasal dari satu jenis perangkat dengan satu pengaturan gain.

#### H27 — Rapikan manifes dan atribusi
Atribusi author BirdCLEF, lisensi per rekaman, klausul aturan kompetisi, CONFIG.TXT AudioMoth per sesi, serta seluruh checksum manifes. Checksum dijalankan sebagai langkah terakhir setelah seluruh data final, bukan di tengah.

#### H28 — Reproduksi segar
Dari klona bersih pada mesin yang berbeda, jalankan satu perintah dan hasilkan kembali satu tabel utama dan satu plot utama. Ini butir wajib quality gate skripsi pada §24 dan merupakan satu-satunya uji yang benar-benar membuktikan reproduktibilitas.
Bila reproduksi gagal, itu temuan yang harus diselesaikan, bukan dilewati dengan menjalankan ulang di mesin asal.

#### H29 — Pembekuan
Bekukan kode, konfigurasi, dan hasil. Beri tag Git pada commit yang menjadi dasar naskah, dan catat tag itu di naskah.

#### H30 — Draft artikel v0.8 dan materi sidang
Periksa §24 dan §25 butir demi butir sebelum menyatakan selesai.

#### Gate 4 — daftar periksa kelulusan
- [ ] Bootstrap berpasangan dengan indeks query sebagai unit resampling.
- [ ] Koreksi Holm diterapkan dan didokumentasikan.
- [ ] CI 95% masuk tabel dan tampil sebagai pita/batang galat pada gambar.
- [ ] Ambang efek minimum ditetapkan sebelum melihat hasil penuh.
- [ ] Seluruh 11 butir gambar dan tabel wajib §18 tersedia atau beralasan.
- [ ] Kata “signifikan” hanya dipakai bila didukung CI berpasangan.
- [ ] Kontaminasi pralatih dibahas eksplisit.
- [ ] Ketidakcocokan geografis dan sidik jari AudioMoth dinyatakan.
- [ ] Manifes, lisensi, atribusi, dan CONFIG.TXT lengkap.
- [ ] Seluruh checksum sinkron dan suite pengujian lulus.
- [ ] Reproduksi segar dari klona bersih berhasil untuk satu tabel dan satu plot.
- [ ] Kode, konfigurasi, dan hasil dibekukan serta diberi tag Git.
- [ ] Seluruh butir §24 terpenuhi.

### Jalur Minimum Bila Tertinggal
Bila jadwal meleset, urutan pengorbanan ditetapkan di muka agar keputusan tidak diambil dalam keadaan panik. Prioritas dari yang paling wajib dipertahankan:
| Prioritas | Komponen | Keputusan bila waktu tidak cukup |
|---|---|---|
| 1 — wajib | E1 clean retrieval + E2 kurva ketahanan SNR | Tidak boleh dikorbankan; ini jawaban RQ1 dan RQ2 |
| 2 — wajib | Statistik berpasangan dengan CI | Tidak boleh dikorbankan; tanpa ini klaim tidak dapat dipertahankan |
| 3 — wajib | E3 open-set dengan τ beku | Boleh disederhanakan menjadi unknown jenis (a) dan (c) saja, jenis (b) ditunda |
| 4 — penting | E5 analisis kegagalan | Pertahankan minimal 20 kasus; jangan diturunkan jumlahnya |
| 5 — dapat diturunkan | E4 pergeseran domain | Boleh turun menjadi pemeriksaan kualitatif, dengan keterbatasan dinyatakan |
| 6 — dapat dibuang | E6 validasi eksternal / ESC-50 | Buang lebih dulu; sifatnya opsional sejak awal |
| 7 — dapat dibuang | Analisis sekunder tipe derau | Buang; datanya tetap tersimpan untuk pengembangan lanjutan |

Yang tidak boleh dilakukan ketika tertinggal: mengurangi jumlah repetisi di bawah rancangan, memilih grid SNR setelah melihat hasil, mengkalibrasi ulang τ pada test set, atau menurunkan jumlah kasus kegagalan di bawah 20. Seluruhnya merusak validitas, bukan sekadar mengurangi cakupan.

### Risiko Minggu 2–4 dan Mitigasinya
| Risiko | Dampak | Mitigasi |
|---|---|---|
| Grid SNR mengalami ceiling atau floor | Kurva ketahanan tidak informatif | Pilot H9 sebelum main run; geser grid lalu bekukan |
| Bank derau tidak cukup untuk seluruh query | E2 tidak lengkap | Pantau kecukupan sejak Minggu 1; rekam lebih banyak daripada target |
| Waktu inferensi R1/R2 terlalu lama | H11–H12 mundur | Ukur waktu pada pilot H9; siapkan cache embedding gallery |
| train_soundscapes terlalu sedikit atau tanpa label memadai | E4 tidak kuantitatif | Nilai kelayakan sudah pada H1; bila tidak memadai, E4 turun menjadi kualitatif |
| CI berpasangan memuat nol | Klaim keunggulan tidak terdukung | Laporkan apa adanya; hasil nol tetap sah menurut §17 |
| Reproduksi segar gagal pada H28 | Quality gate skripsi tidak terpenuhi | Uji klona bersih lebih awal, jangan menunggu H28 |
| Naskah mengklaim lebih dari yang didukung data | Temuan berulang dari tiga audit | Periksa setiap klaim terhadap tabel sebelum submit |

### LAMPIRAN A — REGISTER KEPUTUSAN
| Kode | Keputusan / status | Tindak lanjut |
|---|---|---|
| **DEC-09** | Pivot dataset ke BirdCLEF+ 2026 dan derau AudioMoth | Wajib dicatat pada decision-log.md pada commit yang sama |
| **D-07** | Kepatuhan aturan kompetisi untuk skripsi + artikel | Disetujui (Diarahkan langsung oleh Supervisor 1) |
| **D-08** | Menerima hilangnya kerangka biodiversitas Sumatera dari eksperimen utama | Rekomendasi Supervisor 2: terima |
| **D-09** | Memindahkan E4 ke train_soundscapes BirdCLEF | Rekomendasi Supervisor 2: ya |
| **D-10** | Filter utama collection == XC dan rating >= 3 | Terapkan; bila spesies <15, longgarkan rating ke >=2 dan catat |
| **D-05** | Komposisi dataset lama | Digantikan oleh DEC-09 + scope-freeze v3.0 |
| **D-06** | Rezim hasil lama | Digantikan; hasil lama diarsipkan |
| **D-04** | Status Gate 1 lama | Rekomendasi: tidak lulus dan digantikan Gate 1-R |

### LAMPIRAN B — CHECKLIST PENUTUP AUDIT KEDUA
- [x] D-07 s.d. D-10 diputuskan Supervisor 1 (Diarahkan langsung oleh Supervisor 1 pada arahan audit 12 September 2026).
- [x] DEC-09 tercatat dan scope-freeze v3.0 dibuat.
- [x] BirdCLEF inventory berasal dari skrip.
- [x] Species freeze berasal dari aturan kode.
- [x] Dataset split author-disjoint dan test failure aktif.
- [x] Notebook dan tests memakai satu jalur src/.
- [x] E1 menghasilkan tabel agregat + per-query.
- [ ] AudioMoth memiliki CONFIG.TXT per sesi dan noise manifest lengkap.
- [ ] Pink-noise fallback dihapus/diubah menjadi error (dieksekusi saat AudioMoth tersedia pada H8).
- [x] Hasil Xeno-Canto lama diarsipkan, tidak dihapus.
- [x] Semua manifests dan checksums sinkron.
- [ ] Gate 1-R diverifikasi ulang Supervisor 1.
- [ ] Kedudukan variabel (§10.6) disepakati: konfigurasi AudioMoth adalah variabel kontrol, bukan variabel bebas.
- [ ] Satu konfigurasi AudioMoth dibekukan untuk seluruh bank derau; tidak ada pencampuran pengaturan.
- [ ] Uji kliping per lokasi dilakukan sebelum sesi sebenarnya.
- [ ] Konversi UTC ke WIB dikerjakan di skrip manifes, bukan manual.
- [ ] Grid SNR dibekukan setelah pilot H9 dan tercatat di decision-log.
- [ ] Gate 2, Gate 3, dan Gate 4 diverifikasi Supervisor 1 pada akhir tiap minggu.

### LAMPIRAN C — CATATAN PROVENANS DOKUMEN
Dokumen keputusan kedua ini disusun dari lima sumber internal yang diberikan pada 12 September 2026: audit pertama DSIC-2706, README final revisi pivot, teknis lab Gate 1-R, protokol AudioMoth ITERA, dan lembar inventarisasi BirdCLEF+ 2026. Tidak ada fakta dataset yang belum diinventarisasi yang diperlakukan sebagai terverifikasi.

Pembaruan 12 September 2026 menambahkan tiga hal. Pertama, §10.6 yang menetapkan kedudukan variabel bebas, terikat, dan kontrol, serta menegaskan bahwa seluruh pengaturan AudioMoth berkedudukan sebagai variabel kontrol. Kedua, §2.1.1 sampai §2.1.5 pada Bagian III yang membaca tangkapan layar AudioMoth Configuration App yang diberikan pada tanggal yang sama; pembacaan itu bersifat penilaian terhadap pengaturan yang terlihat di layar, dan nilai yang benar-benar dipakai tetap harus diverifikasi pada perangkat karena pada tangkapan layar tersebut perangkat belum terhubung sehingga Device ID dan versi firmware masih kosong. Ketiga, Bagian V yang memuat rincian hari-ke-hari Minggu 2 sampai Minggu 4 beserta Gate 2, Gate 3, Gate 4, jalur minimum bila tertinggal, dan tabel risiko. Fakta BirdCLEF+ 2026 yang dicatat sebagai terverifikasi berasal dari penelusuran halaman kompetisi Kaggle dan LifeCLEF pada 12 September 2026. Fakta yang belum diverifikasi tetap ditandai sebagai keluaran wajib H1 dan tidak boleh diasumsikan.
