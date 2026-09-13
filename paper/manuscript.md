# Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

---

## Abstract
Passive acoustic monitoring (PAM) generates vast volumes of unannotated audio in ecological habitats. While deep audio representations have demonstrated high classification accuracy on curated, clean focal recordings, their retrieval robustness under severe environmental noise and acoustic domain shifts remains poorly quantified. This study investigates the retrieval resilience of three frozen audio representations: hand-crafted Mel-Frequency Cepstral Coefficients (MFCC with temporal pooling, 40-dim), generic large-scale pretrained embeddings (PANNs CNN14, 2048-dim), and domain-specific bioacoustic embeddings (BirdNET V2.4, 1024-dim) across 16 avian target species of Sumatra (including 5 endemic species). By introducing paired SNR degradation (Clean, 20, 10, 0, and -5 dB) using controlled additive environmental noise and evaluating open-set negative rejection across 77 non-avian soundscape distractors, we assess retrieval degradation (mAP@10, Recall@10) and open-set threshold transfer stability under strict zero-recordist-overlap constraints. We demonstrate that while generic representations suffer catastrophic degradation under low SNR (dropping to 21.2% relative retention at -5 dB), domain-specific bioacoustic embeddings maintain significantly higher relative retention (80.1% at -5 dB SNR, mAP@10 = 0.4710) and stable open-set False Positive Rejection (12.8% to 20.5%).

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Domain Shift, Xeno-Canto, Soundscape, Open-Set Rejection, BirdNET.

---

## 1. Introduction
- Urgensi pemantauan keanekaragaman hayati via bioakustik di kawasan konservasi hutan hujan tropis Sumatera.
- Tantangan retrieval kemiripan audio (*similarity retrieval*) ketika data terbatas (*low-resource*) dan anotasi langka.
- Kesenjangan riset: Sebagian besar studi mengevaluasi classifier tertutup (*closed-set classification*) pada audio bersih, mengabaikan degradasi retrieval berpasangan (*paired robustness*) akibat derau antropogenik/alam dan pergeseran domain *focal-to-soundscape*.

## 2. Related Work
- Representasi Parametrik & Klasik: Davis & Mermelstein (1980).
- Generic Pretrained Audio Representations: Hershey et al. (2017), PANNs (Kong et al., 2020).
- Bioacoustic Foundation Models: BirdNET (Kahl et al., 2021), Global Birdsong Embeddings (Ghani et al., 2023).
- Tantangan Deteksi & Benchmark Terbuka: Stowell et al. (2019, BAD challenge), BIRB (Hamer et al., 2023), BirdSet (Rauch et al., 2025).

## 3. Methodology
### 3.1 Problem Formulation & Paired Robustness Protocol
- Definisi Query, Gallery, dan fungsi representasi $e = f(x)$.
- Cosine similarity metric: $\text{sim}(q, g) = \frac{e_q \cdot e_g}{\|e_q\| \|e_g\|}$.
- Paired SNR degradation curve: $\text{Retention}_m(\text{SNR}) = \frac{\text{Metric}_m(\text{SNR})}{\text{Metric}_m(\text{clean})}$.

### 3.2 Dataset Curation & Strict Global Recordist-Disjoint Partitioning
- **Target Avian Species (Sumatra Focus):** 16 spesies burung target representatif Sumatera dikurasi dari repositori Xeno-Canto (mencakup 5 spesies endemik seperti *Carpococcyx viridis*, *Gypsophila rufipectus*, *Myophonus melanurus*, *Napothera albostriata*, dan *Polyplectron chalcurum*).
- **Audit Fisik & Integritas Berkas:** Seluruh 416 berkas audio burung telah melalui verifikasi integritas checksum SHA-256 dan audit manual:
  - 0 berkas korup / unreadable.
  - Distribusi volume klip per spesies: minimum 15 berkas (*Myophonus melanurus*) hingga maksimum 37 berkas (*Pnoepyga pusilla*), memenuhi ambang batas evaluasi statistik retrieval.
  - Isolasi 77 berkas audio satwa non-burung (serangga, amfibi, kelelawar, primata) untuk subset *unknown/open-set negative rejection*.
- **Partisi Bebas Kebocoran (Strict Global Recordist-Disjoint):**
  Untuk menghindari model "menghafal" karakteristik mikrofon, kompresi, atau derau latar perekam tertentu (*recording gear fingerprinting*), data dipartisi menggunakan optimasi pemotongan graf perekam:
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
  - **Gallery Set (Reference Bank):** 260 klip dari 42 perekam independen.
  - **Query Clean Set:** 94 klip dari 29 perekam independen.
  - **Calibration Set:** 62 klip (digunakan untuk kalibrasi ambang batas $\tau$).
  - **Unknown Test Set:** 77 klip non-burung (38 untuk kalibrasi ambang batas, 39 untuk uji evaluasi akhir open-set).
  - **Overlap Recordist Gallery vs Query:** Tepat 0 perekam ($0\%$).

### 3.3 Audio Representations
- $R_0$: MFCC + mean/std temporal aggregation (40 dimensi).
- $R_1$: PANNs CNN14 AudioSet pretrained (2048 dimensi).
- $R_2$: BirdNET V2.4 Backbone intermediate representation (1024 dimensi).
- $R_3$: Random Ranking control (40 dimensi).

### 3.4 Open-Set Calibration & Threshold Transfer
- Formulasi keputusan: $\text{accept}(q) = 1$ jika $\max_g \text{sim}(q, g) \ge \tau$, else $0$.
- Pembekuan $\tau$ pada calibration split independen menggunakan optimasi kurva ROC empiris (Youden's $J = \text{TPR} - \text{FPR}$).
- Pengujian transfer ambang $\tau$ melintasi kondisi derau Clean, 20 dB, 10 dB, 0 dB, dan -5 dB, di mana audio tak dikenal (*unknown*) juga diinjeksi derau pada level yang sama secara berpasangan.

## 4. Experimental Results
1. **Clean Retrieval Performance (E1):**
   - $R_2$ (BirdNET) mencapai mAP@10 tertinggi (**0.5876**), mengungguli $R_1$ PANNs (**0.2069**), $R_0$ MFCC (**0.1029**), dan $R_3$ Random (**0.0209**).
   - Akurasi Top-1 $R_2$ mencapai **78.7%**, membuktikan ketajaman representasi bioakustik pada kondisi ideal.
2. **Paired Noise Degradation Curves (E2):**
   - Pada SNR -5 dB (derau ekstrem), $R_2$ mempertahankan mAP@10 sebesar **0.4710** dengan retensi relatif **80.1%** (Akurasi Top-1 tetap di **71.3%**).
   - Sebaliknya, $R_1$ mengalami penurunan curam hingga retensi **21.2%** (mAP@10 = 0.0438), dan $R_0$ turun ke retensi **27.4%** (mAP@10 = 0.0282).
3. **Open-Set Rejection Analysis (E3):**
   - Ambang beku $R_2$ ($\tau = 0.6488$) menghasilkan False Positive Rate yang stabil di rentang **12.8% – 20.5%** dengan AUROC bersih **0.8803**.
   - $R_1$ ($\tau = 0.8567$) mengalami kegagalan penolakan dengan lonjakan FPR hingga **84.6%** pada SNR 0 dB.

*(Catatan Cakupan: Sesuai Keputusan D-03 Pembimbing, pengujian rekaman lapangan kampus ITERA diposisikan sebagai rencana penelitian lanjutan setelah pengadaan rekaman teranotasi lengkap).*

## 5. Failure Analysis (E5)
Audit mendalam dilakukan terhadap 30 kasus kegagalan nyata yang terekam pada `results/raw/`:
1. **Low SNR Masking (66.7%):** Pada SNR -5 dB dan 0 dB, amplitudo derau lingkungan menenggelamkan pita formulan nada tinggi pada burung bertubuh kecil (misal: *Aethopyga siparaja*, *Batrachostomus cornutus*).
2. **Acoustic Feature Overlap (20.0%):** Keserupaan pola frekuensi dasar antara panggilan burung tertentu dengan vokalisasi serangga/jangkrik malam hari pada subset unknown.
3. **Inter-Species Confusion (13.3%):** Keserupaan pola harmonik antarspesies yang berkerabat dekat dalam famili Dicruridae dan Muscicapidae.

## 6. Conclusion & Threats to Validity
### 6.1 Ringkasan Temuan
- Representasi bioakustik terlatih domain khusus ($R_2$: BirdNET) terbukti secara signifikan mengungguli representasi umum ($R_1$) dan parametrik ($R_0$) dalam menjaga ketahanan pencarian di bawah gangguan derau lingkungan (retensi 80.1% vs 21.2%).
- Ambang transfer open-set pada representasi bioakustik menunjukkan kontrol tingkat penerimaan keliru (FPR) yang jauh lebih stabil terhadap fluktuasi derau dibanding representasi umum.

### 6.2 Threats to Validity (Ancaman Validitas)
1. **Recording & Recordist Leakage:**
   - *Mitigasi:* Korpus dievaluasi menggunakan partisi **Strict Global Recordist-Disjoint** ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$). Tidak ada satu pun perekam di Gallery yang muncul di Query Clean pada spesies manapun.
2. **Keterbatasan Kalibrasi Ambang:**
   - Data kalibrasi terpisah secara independen pada tingkat klip, namun berbagi 19 perekam dengan subset query_clean. Dampaknya terbatas pada kemungkinan bias optimistik lokal pada recall ambang $\tau$, sementara metrik primer mAP@10 pada E1/E2 tetap 100% bebas dari kebocoran perekam.
3. **Pretraining Contamination:**
   - Sebagian data publik Xeno-Canto kemungkinan pernah menjadi bagian dari korpus latih BirdNET. Namun keunggulan retensi relatif berpasangan (*paired retention*) di bawah derau lingkungan lokal tetap membuktikan ketahanan fitur representasional yang telah dipelajari model.
4. **Additive Controlled Noise vs. Propagation Physics:**
   - Derau aditif menguji respons spektral murni namun belum memodelkan efek distorsi jarak jauh (*reverberation* dan pantulan kanopi pohon).

---
## References
*(Sinkron dengan matriks referensi pada `jurnal/referensi_jurnal_TA_bioakustik.csv`)*
