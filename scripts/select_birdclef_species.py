from pathlib import Path
import pandas as pd
# 1. Tentukan path root repositori
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "BirdClef"
MANIFEST_DIR = REPO_ROOT / "data" / "manifests"
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
TRAIN_CSV = DATA_DIR / "train.csv"
TAXONOMY_CSV = DATA_DIR / "taxonomy.csv"
def main():
    print("=" * 70)
    print("[*] MEMULAI SELEKSI SPESIES TARGET BIRDCLEF+ 2026 (ATURAN H2)")
    print("=" * 70)
    if not TRAIN_CSV.exists():
        raise FileNotFoundError(f"Berkas tidak ditemukan: {TRAIN_CSV}")
    df_train = pd.read_csv(TRAIN_CSV)
    print(f"[+] Total rekaman mentah di train.csv: {len(df_train):,} baris")
    # Filter author Unknown
    df_clean = df_train[df_train["author"].str.strip().str.lower() != "unknown"].copy()
    print(f"[+] Rekaman setelah menghapus author Unknown: {len(df_clean):,} baris")
    # Kriteria Audit H2
    mask_aves = df_clean["class_name"] == "Aves"
    mask_xc = df_clean["collection"] == "XC"
    mask_rating = df_clean["rating"] >= 3.0
    df_eligible = df_clean[mask_aves & mask_xc & mask_rating].copy()
    print(f"[+] Rekaman lolos kriteria (Aves + XC + rating >= 3.0): {len(df_eligible):,} baris")
    # Agregasi statistik per spesies
    sp_stats = df_eligible.groupby(["primary_label", "scientific_name", "common_name"]).agg(
        n_klip=("filename", "count"),
        n_author=("author", "nunique"),
        rating_median=("rating", "median")
    ).reset_index()
    # Ambang kecukupan volume
    mask_volume = (sp_stats["n_klip"] >= 20) & (sp_stats["n_author"] >= 3)
    valid_species = sp_stats[mask_volume].copy()
    print(f"[+] Spesies burung yang memenuhi seluruh ambang (n_klip >= 20 & n_author >= 3): {len(valid_species)} spesies")
    # Pilih 20 taksa dengan diversitas author independen tertinggi
    top20_species = valid_species.sort_values(
        by=["n_author", "n_klip", "primary_label"],
        ascending=[False, False, True]
    ).head(20).reset_index(drop=True)
    # Simpan species_freeze.csv
    freeze_csv = MANIFEST_DIR / "species_freeze.csv"
    top20_species.rename(columns={"primary_label": "species_key"}, inplace=True)
    top20_species.to_csv(freeze_csv, index=False)
    print(f"\n[+] BERHASIL: 20 Spesies target dibekukan di: {freeze_csv}")
    # Catat spesies yang dikeluarkan (species_excluded.csv)
    selected_keys = set(top20_species["species_key"])
    
    # Kumpulkan seluruh taksa unik dari dataset mentah untuk identifikasi alasan eksklusi
    all_species_raw = df_train.groupby(["primary_label", "scientific_name", "common_name", "class_name"]).agg(
        total_klip=("filename", "count"),
        xc_klip=("collection", lambda x: (x == "XC").sum()),
        n_author_raw=("author", "nunique")
    ).reset_index()
    
    # Statistik dari rekaman bermutu (Aves + XC + rating >= 3.0) untuk pengecekan ambang yang konsisten
    eligible_stats = df_eligible.groupby("primary_label").agg(
        eligible_klip=("filename", "count"),
        eligible_author=("author", "nunique"),
        eligible_rating_median=("rating", "median")
    ).reset_index()
    eligible_lookup = dict(zip(eligible_stats["primary_label"], eligible_stats.itertuples(index=False)))
    
    excluded = []
    for _, row in all_species_raw.iterrows():
        sp = row["primary_label"]
        if sp in selected_keys:
            continue
        
        reasons = []
        # Alasan substantif: taksa ini bukan burung
        if row["class_name"] != "Aves":
            reasons.append(f"Non-Aves ({row['class_name']})")
        # Alasan substantif: tidak ada rekaman XC sama sekali
        if row["xc_klip"] == 0:
            reasons.append("Bukan koleksi XC")
        
        # Cek statistik dari rekaman bermutu (bukan mentah)
        el = eligible_lookup.get(sp, None)
        if el is None:
            # Tidak punya satupun rekaman Aves+XC+rating>=3.0
            if row["class_name"] == "Aves" and row["xc_klip"] > 0:
                reasons.append("Tidak ada rekaman XC dengan rating >= 3.0")
        else:
            # Punya rekaman bermutu -- cek ambang volume
            if el.eligible_klip < 20:
                reasons.append(f"Klip bermutu < 20 ({el.eligible_klip})")
            if el.eligible_author < 3:
                reasons.append(f"Author bermutu < 3 ({el.eligible_author})")
        
        # Jika tidak ada alasan substantif, berarti lolos semua ambang tapi kalah ranking
        if not reasons:
            reasons.append("Di luar kuota Top 20 author diversitas tertinggi")
        
        excluded.append({
            "species_key": sp,
            "scientific_name": row["scientific_name"],
            "common_name": row["common_name"],
            "alasan_eksklusi": "; ".join(reasons)
        })
    df_excluded = pd.DataFrame(excluded)
    excluded_csv = MANIFEST_DIR / "species_excluded.csv"
    df_excluded.to_csv(excluded_csv, index=False)
    print(f"[+] BERHASIL: {len(df_excluded)} Spesies non-target dicatat di: {excluded_csv}")
    print("\n" + "=" * 70)
    print("DAFTAR 20 SPESIES BURUNG TARGET TERPILIH:")
    print("=" * 70)
    for idx, row in top20_species.iterrows():
        print(f"{idx+1:2d}. [{row['species_key']:7s}] {row['scientific_name']:<30s} | Klip: {row['n_klip']:3d} | Author: {row['n_author']:3d} | Median Rating: {row['rating_median']:.1f}")
    print("=" * 70)
if __name__ == "__main__":
    main()