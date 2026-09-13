
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""
Script: src/plot_results.py
Fungsi: Menghasilkan grafik ilmiah wajib (Bab 18 Dokumen Audit):
1. Kurva Ketahanan Retrieval (mAP@10 vs SNR)
2. Plot Retensi Relatif terhadap Kondisi Bersih (Relative Retention vs SNR)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = str(PROJECT_ROOT / "results/processed")
FIG_DIR = str(PROJECT_ROOT / "results/figures")
os.makedirs(FIG_DIR, exist_ok=True)

def generate_all_figures():
    os.makedirs(FIG_DIR, exist_ok=True)
    table_path = os.path.join(RESULTS_DIR, "snr_robustness_table.csv")
    if not os.path.exists(table_path):
        print(f"[!] File {table_path} belum ada, grafik tidak dapat digenerate.")
        return False

    df_snr = pd.read_csv(table_path)

    # Urutan kondisi: Clean (direpresentasikan 30 dB untuk visualisasi kurva kontinyu), 20, 10, 0, -5
    condition_order = ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]
    snr_x_labels = ["Clean", "20 dB", "10 dB", "0 dB", "-5 dB"]
    x_pos = [0, 1, 2, 3, 4]

    colors = {
        "R0": "#1f77b4",  # MFCC (Biru)
        "R1": "#ff7f0e",  # Generic (Oranye)
        "R2": "#2ca02c",  # Bioacoustic (Hijau)
        "R3": "#d62728"   # Random Control (Merah)
    }

    labels = {
        "R0": "R0: MFCC Baseline (40-dim)",
        "R1": "R1: Generic Audio (PANNs-like)",
        "R2": "R2: Bioacoustic Pretrained",
        "R3": "R3: Random Ranking (Control)"
    }

    # 1. Plot mAP@10 vs SNR
    plt.figure(figsize=(9, 5.5), dpi=150)
    for rep in ["R0", "R1", "R2", "R3"]:
        sub = df_snr[df_snr["representation"] == rep].copy()
        sub["sort_key"] = sub["condition"].map(lambda c: condition_order.index(c) if c in condition_order else 99)
        sub = sub.sort_values("sort_key")
        plt.plot(x_pos, sub["mAP@10"], marker='o', linewidth=2.2, markersize=7, color=colors[rep], label=labels[rep])

    plt.xticks(x_pos, snr_x_labels, fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel("Kondisi Derau Lingkungan (SNR)", fontsize=12, fontweight='bold')
    plt.ylabel("mAP@10 (Mean Average Precision)", fontsize=12, fontweight='bold')
    plt.title("Ketahanan Representasi Audio terhadap Peningkatan Derau (DSIC27-06)", fontsize=13, fontweight='bold', pad=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, fontsize=10, loc="upper right")
    plt.tight_layout()
    map_fig_path = os.path.join(FIG_DIR, "robustness_curve_map10.png")
    plt.savefig(map_fig_path)
    plt.close()
    print(f"[+] Grafik mAP@10 tersimpan di: {map_fig_path}")

    # 2. Plot Relative Retention vs SNR
    plt.figure(figsize=(9, 5.5), dpi=150)
    for rep in ["R0", "R1", "R2"]:  # Tanpa R3 agar skala relevan
        sub = df_snr[df_snr["representation"] == rep].copy()
        sub["sort_key"] = sub["condition"].map(lambda c: condition_order.index(c) if c in condition_order else 99)
        sub = sub.sort_values("sort_key")
        plt.plot(x_pos, sub["relative_retention"] * 100, marker='s', linewidth=2.2, markersize=7, color=colors[rep], label=labels[rep])

    plt.axhline(100, color="gray", linestyle=":", alpha=0.7)
    plt.xticks(x_pos, snr_x_labels, fontsize=11)
    plt.yticks(range(0, 121, 20), fontsize=11)
    plt.xlabel("Kondisi Derau Lingkungan (SNR)", fontsize=12, fontweight='bold')
    plt.ylabel("Retensi Performa Relatif (% terhadap Clean)", fontsize=12, fontweight='bold')
    plt.title("Kurva Penurunan Kualitas Retrieval Relatif (Retention Curve)", fontsize=13, fontweight='bold', pad=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, fontsize=10, loc="lower left")
    plt.tight_layout()
    ret_fig_path = os.path.join(FIG_DIR, "relative_retention_curve.png")
    plt.savefig(ret_fig_path)
    plt.close()
    print(f"[+] Grafik Retensi Relatif tersimpan di: {ret_fig_path}")
    return True


if __name__ == "__main__":
    generate_all_figures()
