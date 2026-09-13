# Eksperimen E1 — Clean Retrieval Benchmark

## 1. Tujuan Ilmiah
Membangun tolok ukur dasar (*clean baseline*) kemampuan perolehan kemiripan (*similarity retrieval*) dari representasi audio terstandardisasi pada kondisi ideal (rekaman bersih bebas derau tambahan) lintas 20 spesies burung target korpus BirdCLEF+ 2026.

## 2. Konfigurasi Eksperimen
* **Data Uji:** 200 kueri bersih (tepat 10 kueri per spesies dari 68 perekam independen).
* **Data Referensi (Gallery):** 3.653 rekaman galeri dari 377 perekam independen.
* **Representasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 (2048-dim)
  * $R_2$: BirdNET Backbone (1024-dim)
  * $R_3$: Random Control (40-dim)
* **Metrik Kesamaan:** Cosine Similarity ($200 \times 3.653$ pairwise similarity matrix).

## 3. Eksekusi & Hasil Kanonikal
* **Notebook:** [`notebooks/E1_Clean_Retrieval.ipynb`](../../notebooks/E1_Clean_Retrieval.ipynb)
* **Tabel Hasil Resmi (`results/processed/clean_retrieval_table.csv`):**

| Representasi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **$R_2$: BirdNET Backbone (1024-d)** | **95.0%** | **0.9126** | **0.9658** | **0.9280** | **0.0528** |
| **$R_1$: PANNs CNN14 (2048-d)** | **60.0%** | **0.4152** | **0.7005** | **0.5025** | **0.0291** |
| **$R_0$: MFCC Baseline (40-d)** | **27.5%** | **0.1319** | **0.4224** | **0.2175** | **0.0123** |
| **$R_3$: Random Control (40-d)** | **6.5%** | **0.0190** | **0.1779** | **0.0530** | **0.0028** |

* **Log Granular (Audit H5.2):** Tersimpan di [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) (800 baris memuat kolom `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, `AP@10`).
* **Visualisasi:** Tersimpan di [`results/figures/clean_retrieval_benchmark.png`](../../results/figures/clean_retrieval_benchmark.png).

## 4. Status Kelulusan
**LULUS 100% (Gate 1-R)**.
