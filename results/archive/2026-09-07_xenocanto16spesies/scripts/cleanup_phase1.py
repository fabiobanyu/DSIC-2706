"""
Skrip Fase 1: Pembersihan Artefak Dummy & Pemeriksaan Jalur Windows
Topik: DSIC-2706 (Audit 2026-09-07)
"""

from pathlib import Path

# Mendapatkan root direktori proyek secara otomatis (bebas hardcoded path)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 1. Daftar berkas dummy / usang yang harus dibersihkan
files_to_remove = [
    PROJECT_ROOT / "results/processed/failure_analysis_table.csv",
    PROJECT_ROOT / "results/tables/failure_analysis_table.csv",
    PROJECT_ROOT / "results/failure_cases/failure_analysis_table.csv",
    PROJECT_ROOT / "paper/tables/failure_analysis_table.csv",
    PROJECT_ROOT / "results/processed/openset_evaluation_table.csv",
    PROJECT_ROOT / "results/tables/openset_evaluation_table.csv",
    PROJECT_ROOT / "paper/tables/openset_evaluation_table.csv",
    PROJECT_ROOT / "jurnal/referensi_jurnal_TA_bioakustik (1).csv",
]

print("=" * 60)
print("=== [FASE 1.1] PEMBERSIHAN ARTEFAK DUMMY & USANG ===")
print("=" * 60)
for p in files_to_remove:
    if p.exists():
        p.unlink()
        print(f"[BERHASIL DIHAPUS] {p.relative_to(PROJECT_ROOT)}")
    else:
        print(f"[SUDAH BERSIH / TIDAK ADA] {p.relative_to(PROJECT_ROOT)}")

print("\n" + "=" * 60)
print("=== [FASE 1.2] PEMERIKSAAN JALUR ABSOLUT WINDOWS (M-07) ===")
print("=" * 60)
py_files = list((PROJECT_ROOT / "src").glob("*.py")) + list((PROJECT_ROOT / "experiments").glob("**/*.py"))
hardcoded_found = []

for f in py_files:
    if f.is_file():
        content = f.read_text(encoding="utf-8", errors="ignore")
        if "FILE AND TASK" in content or "d:/" in content.lower():
            hardcoded_found.append(f)
            print(f"[PERLU DINORMALISASI] {f.relative_to(PROJECT_ROOT)}")

if not hardcoded_found:
    print("[SEMUA AMAN] Tidak ada hardcoded path di folder src/ dan experiments/!")
else:
    print(f"\nTotal {len(hardcoded_found)} berkas perlu dinormalisasi path-nya ke root proyek.")
print("=" * 60)
