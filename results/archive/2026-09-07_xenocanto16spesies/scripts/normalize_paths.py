"""
Skrip Fase 1.2: Normalisasi Jalur Absolut Windows ke Jalur Portabel Proyek (M-07)
Topik: DSIC-2706
"""

from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

print("=" * 60)
print("=== [FASE 1.2] NORMALISASI JALUR ABSOLUT WINDOWS KE PORTABEL ===")
print("=" * 60)

# 1. Normalisasi file_path di data/manifests/dataset_split.csv
split_csv = PROJECT_ROOT / "data/manifests/dataset_split.csv"
if split_csv.exists():
    df = pd.read_csv(split_csv)
    original_sample = df["file_path"].iloc[0]
    
    # Ubah path absolut menjadi relative POSIX path (data/xeno_canto/...)
    def make_relative_posix(path_str):
        if not isinstance(path_str, str) or not path_str:
            return path_str
        # Bersihkan awalan d:/...
        p = re.sub(r"^[a-zA-Z]:[/\\].*?[/\\]TA[/\\]?", "", path_str)
        # Normalisasi separator menjadi forward slash '/'
        p = p.replace("\\", "/").lstrip("/")
        return p

    df["file_path"] = df["file_path"].apply(make_relative_posix)
    df.to_csv(split_csv, index=False)
    print(f"[BERHASIL] data/manifests/dataset_split.csv dinormalisasi:")
    print(f"  Sebelum: {original_sample}")
    print(f"  Sesudah: {df['file_path'].iloc[0]}")
else:
    print("[LEWAT] dataset_split.csv tidak ditemukan.")

# 2. Normalisasi skrip-skrip di src/
src_files = list((PROJECT_ROOT / "src").glob("*.py"))
modified_count = 0

for f in src_files:
    content = f.read_text(encoding="utf-8")
    if "FILE AND TASK" in content or "d:/" in content.lower():
        # Tambahkan PROJECT_ROOT jika belum ada
        lines = content.splitlines()
        new_lines = []
        has_pathlib = "from pathlib import Path" in content
        
        # Ganti pola d:/FILE AND TASK/TA/...
        modified_content = content
        # Tangani sys.path.insert(0, "d:/FILE AND TASK/TA")
        modified_content = re.sub(
            r'sys\.path\.insert\(0,\s*["\']d:/FILE AND TASK/TA["\']\)',
            'sys.path.insert(0, str(Path(__file__).resolve().parent.parent))',
            modified_content,
            flags=re.IGNORECASE
        )
        # Tangani path string variabel
        modified_content = re.sub(
            r'["\']d:/FILE AND TASK/TA/([^"\']+)["\']',
            r'str(PROJECT_ROOT / "\1")',
            modified_content,
            flags=re.IGNORECASE
        )
        # Tangani path di mkdir/makedirs
        modified_content = re.sub(
            r'os\.makedirs\(["\']d:/FILE AND TASK/TA/([^"\']+)["\']',
            r'os.makedirs(str(PROJECT_ROOT / "\1")',
            modified_content,
            flags=re.IGNORECASE
        )
        
        # Pastikan PROJECT_ROOT didefinisikan di dekat awal file
        if "PROJECT_ROOT" in modified_content and "PROJECT_ROOT = " not in modified_content:
            # Sisipkan import Path dan PROJECT_ROOT setelah import standard
            import_block = "\nfrom pathlib import Path\nPROJECT_ROOT = Path(__file__).resolve().parent.parent\n"
            if not has_pathlib:
                modified_content = import_block + modified_content
            else:
                modified_content = re.sub(r'(from pathlib import Path.*?\n)', r'\1PROJECT_ROOT = Path(__file__).resolve().parent.parent\n', modified_content, count=1)

        f.write_text(modified_content, encoding="utf-8")
        print(f"[DIPERBAIKI] {f.relative_to(PROJECT_ROOT)}")
        modified_count += 1

# 3. Pastikan src/preprocess.py menangani path relatif terhadap PROJECT_ROOT
preprocess_py = PROJECT_ROOT / "src/preprocess.py"
if preprocess_py.exists():
    p_content = preprocess_py.read_text(encoding="utf-8")
    if "if not os.path.isabs(file_path):" not in p_content:
        # Tambahkan resolusi path otomatis
        target_check = 'if not os.path.exists(file_path):'
        replacement = 'if not os.path.isabs(file_path):\n        file_path = os.path.join(str(PROJECT_ROOT), file_path)\n    if not os.path.exists(file_path):'
        p_content = p_content.replace(target_check, replacement, 1)
        preprocess_py.write_text(p_content, encoding="utf-8")
        print("[BERHASIL] src/preprocess.py diperbarui untuk mendukung path relatif.")

print("\n" + "=" * 60)
print(f"Selesai! Total {modified_count} berkas berhasil dinormalisasi.")
print("Semua path sekarang berbasis Path(__file__).resolve().parent.parent (Cross-Platform).")
print("=" * 60)
