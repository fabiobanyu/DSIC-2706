"""
Script: scripts/update_manifest_hashes.py
Fungsi: Menghitung ulang dan mencatat hash integritas SHA-256 ketiga manifes resmi.
Menyelesaikan temuan audit M-06.
Perintah pembuatan: python scripts/update_manifest_hashes.py
"""

import hashlib
from pathlib import Path
import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data/manifests"
OUTPUT_FILE = PROJECT_ROOT / "artifacts/reproducibility/manifest_sha256.txt"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

manifest_files = [
    "dataset_split.csv",
    "species_freeze.csv",
    "species_excluded.csv",
    "itera_noise_manifest.csv",
]

def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 70)
    print("=== PENGHITUNGAN ULANG SHA-256 MANIFES INTEGRITAS (M-06) ===")
    print("=" * 70)

    lines = [
        "# Rekam Jejak Audit Integritas & Reproducibility DSIC-2706",
        f"# Tanggal: {datetime.date.today().strftime('%d %B %Y')}",
        "# Perintah Pembuat: python scripts/update_manifest_hashes.py",
        "",
    ]

    for fname in manifest_files:
        fpath = MANIFEST_DIR / fname
        if not fpath.exists():
            continue
        sha = get_file_sha256(fpath)
        lines.append(f"{fname} : {sha}")
        print(f"[+] {fname:<30} : {sha}")

    # Baseline E1: baca dari hasil eksperimen aktual (bukan hardcode)
    e1_csv = PROJECT_ROOT / "results/processed/clean_retrieval_table.csv"
    if e1_csv.exists():
        import csv
        with open(e1_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            lines.append("")
            lines.append("# Baseline Verifikasi E1 Clean Retrieval (dari results/processed/clean_retrieval_table.csv):")
            for row in reader:
                name = row.get("name", row.get("representation", ""))
                top1 = row.get("Top1_Accuracy", "")
                mAP = row.get("mAP@10", "")
                mrr = row.get("MRR", "")
                lines.append(f"{name} : Top1={top1}% mAP@10={mAP} MRR={mrr}")
            lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"[SUKSES] Hash integritas berhasil diperbarui di: {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
