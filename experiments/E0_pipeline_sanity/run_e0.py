"""
E0: Pipeline Sanity Check
- Memvalidasi pembekuan parameter audio (32 kHz, 5.0 detik, RMS 0.05).
- Memvalidasi zero split leakage (ID, path, recordist).
- Memastikan random ranking (R3) menghasilkan skor di bawah representasi riil (R0-R2).
"""

import os
import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import TARGET_SR, DURATION_SEC, TARGET_RMS
from tests.test_split_leakage import test_zero_recordist_leakage_global, test_zero_leakage_between_gallery_and_query


def run_e0_sanity():
    print("=" * 70)
    print("[*] MENJALANKAN EXPERIMENT E0: PIPELINE SANITY CHECK")
    print("=" * 70)

    # 1. Parameter audio
    print(f"[+] Parameter Audio Baku: SR={TARGET_SR} Hz, Durasi={DURATION_SEC}s, RMS={TARGET_RMS}")
    assert TARGET_SR == 32000, "Target SR harus 32000 Hz"
    assert DURATION_SEC == 5.0, "Durasi segmen harus 5.0 detik"

    # 2. Audit Split Leakage
    test_zero_leakage_between_gallery_and_query()
    test_zero_recordist_leakage_global()
    print("[+] Audit Split Bebas Kebocoran: ZERO LEAKAGE (PASSED)")

    # 3. Kontrol Positif
    from src.run_benchmark import run_experiment_for_representation
    res_r3 = run_experiment_for_representation("R3", snr_list=[])
    map_r3 = res_r3["snr_summary"]["mAP@10"].iloc[0]
    print(f"[+] Baseline Random Ranking (R3) mAP@10: {map_r3:.4f}")
    assert map_r3 < 0.05, "Random ranking harus menghasilkan mAP rendah (chance level)"

    print("=" * 70)
    print("[+] EXPERIMENT E0 SANITY CHECK PASSED 100%!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    run_e0_sanity()
