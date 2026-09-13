"""
Unit Test: tests/test_snr_mixing.py
Memvalidasi keakuratan formula SNR mixing dan determinisme random seed.
"""

import sys
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.mix_noise import mix_audio_at_snr, compute_signal_power


def test_snr_mixing_accuracy():
    sr = 32000
    duration = 2.0
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    clean = (0.5 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)

    for target_snr in [20, 10, 0]:
        noise = np.random.randn(len(clean)).astype(np.float32)
        p_c = compute_signal_power(clean)
        p_n = compute_signal_power(noise)
        alpha = np.sqrt(p_c / (p_n * 10.0 ** (target_snr / 10.0)))
        mixed = clean + alpha * noise

        # Komponen sinyal dan derau murni
        actual_snr = 10 * np.log10(p_c / compute_signal_power(alpha * noise))
        assert abs(actual_snr - target_snr) < 1e-4, f"Target {target_snr} dB, tetapi formula {actual_snr:.2f} dB"


def test_snr_mixing_reproducibility():
    clean = np.random.randn(32000).astype(np.float32)
    m1 = mix_audio_at_snr(clean, snr_db=10, seed=99)
    m2 = mix_audio_at_snr(clean, snr_db=10, seed=99)
    m3 = mix_audio_at_snr(clean, snr_db=10, seed=100)

    # Seed sama harus menghasilkan sinyal identik
    np.testing.assert_allclose(m1, m2, err_msg="Seed yang sama harus menghasilkan sinyal identik!")
    # Seed beda harus menghasilkan sinyal berbeda
    assert not np.allclose(m1, m3), "Seed berbeda harus menghasilkan derau yang berbeda!"
