import os
from pathlib import Path
import pandas as pd


def _get_split_path() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent, current.parent.parent, current.parent.parent.parent]:
        target = parent / "data" / "manifests" / "dataset_split.csv"
        if target.exists():
            return target
    raise FileNotFoundError(f"Manifes dataset_split.csv tidak ditemukan dari lokasi {current}!")


SPLIT_PATH = _get_split_path()


def test_zero_leakage_between_gallery_and_query():
    """Memverifikasi zero ID overlap antara Gallery, Query, dan Calibration."""
    df = pd.read_csv(SPLIT_PATH)
    id_col = "recording_id" if "recording_id" in df.columns else "id"
    gallery_ids = set(df[df['split_role'] == 'gallery'][id_col].astype(str))
    query_ids = set(df[df['split_role'] == 'query_clean'][id_col].astype(str))
    calib_ids = set(df[df['split_role'] == 'calibration'][id_col].astype(str))
    
    # 1. Gallery vs Query
    overlap_g_q = gallery_ids.intersection(query_ids)
    assert len(overlap_g_q) == 0, f"Ditemukan kebocoran {len(overlap_g_q)} ID rekaman antara Gallery dan Query: {overlap_g_q}"
    
    # 2. Gallery vs Calibration
    overlap_g_c = gallery_ids.intersection(calib_ids)
    assert len(overlap_g_c) == 0, f"Ditemukan kebocoran {len(overlap_g_c)} ID rekaman antara Gallery dan Calibration: {overlap_g_c}"
    
    # 3. Query vs Calibration
    overlap_q_c = query_ids.intersection(calib_ids)
    assert len(overlap_q_c) == 0, f"Ditemukan kebocoran {len(overlap_q_c)} ID rekaman antara Query dan Calibration: {overlap_q_c}"


def test_zero_filepath_leakage():
    """Memverifikasi zero file_path overlap antara Gallery, Query, dan Calibration."""
    df = pd.read_csv(SPLIT_PATH)
    gallery_paths = set(df[df['split_role'] == 'gallery']['file_path'].dropna())
    query_paths = set(df[df['split_role'] == 'query_clean']['file_path'].dropna())
    calib_paths = set(df[df['split_role'] == 'calibration']['file_path'].dropna())
    
    assert len(gallery_paths.intersection(query_paths)) == 0, "Ditemukan kebocoran path berkas antara Gallery dan Query"
    assert len(gallery_paths.intersection(calib_paths)) == 0, "Ditemukan kebocoran path berkas antara Gallery dan Calibration"
    assert len(query_paths.intersection(calib_paths)) == 0, "Ditemukan kebocoran path berkas antara Query dan Calibration"


def test_zero_recordist_leakage_global():
    """Memverifikasi strict global recordist/author disjoint di ketiga subset (0 author overlap)."""
    df = pd.read_csv(SPLIT_PATH)
    rec_col = "author" if "author" in df.columns else "recordist"
    
    # Penanganan eksplisit author == "Unknown" (Audit H2.1 & H3.2, Checklist Gate 1-R)
    # Rekaman dengan author tak dikenal (Unknown/NaN/kosong) tidak boleh masuk ke split
    # untuk mencegah pengelompokan semu atau lolos/gagal kebocoran secara semu.
    unknown_mask = df[rec_col].astype(str).str.strip().str.lower().isin(["unknown", "nan", "none", ""])
    assert not unknown_mask.any(), (
        f"[H2.1/H3.2 AUDIT ERROR] Ditemukan {unknown_mask.sum()} rekaman dengan author == 'Unknown' "
        f"atau kosong pada {SPLIT_PATH.name}!"
    )

    gallery_recs = set(df[df['split_role'] == 'gallery'][rec_col].dropna().unique())
    query_recs = set(df[df['split_role'] == 'query_clean'][rec_col].dropna().unique())
    calib_recs = set(df[df['split_role'] == 'calibration'][rec_col].dropna().unique())
    
    overlap_g_q = gallery_recs.intersection(query_recs)
    assert len(overlap_g_q) == 0, f"Ditemukan kebocoran author antara Gallery dan Query: {overlap_g_q}"
    
    overlap_g_c = gallery_recs.intersection(calib_recs)
    assert len(overlap_g_c) == 0, f"Ditemukan kebocoran author antara Gallery dan Calibration: {overlap_g_c}"
    
    overlap_q_c = query_recs.intersection(calib_recs)
    assert len(overlap_q_c) == 0, f"Ditemukan kebocoran author antara Query dan Calibration: {overlap_q_c}"


