"""Módulo para la atenuación de interferencia de línea eléctrica (50 Hz y armónicos)."""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def main():
    """Diseña y aplica filtros rechaza-banda en cascada para limpiar la señal útil."""
    fs = 1000.0
    t = np.arange(0, 2.0, 1 / fs)

    senal_util = 1.0 * np.sin(2 * np.pi * 17 * t)
    interferencia = 0.6 * np.sin(2 * np.pi * 50 * t) + 0.3 * np.sin(2 * np.pi * 150 * t)
    senal_sucia = senal_util + interferencia

    # 1. Diseñar y aplicar rechaza-banda en cascada
    # Filtro 50 Hz
    b50, a50 = signal.butter(4, [45, 55], btype='bandstop', fs=fs)
    senal_f1 = signal.filtfilt(b50, a50, senal_sucia)

    # Filtro 150 Hz
    b150, a150 = signal.butter(4, [145, 155], btype='bandstop', fs=fs)
    senal_limpia = signal.filtfilt(b150, a150, senal_f1)

    # 2. Análisis espectral antes y después
    frec_antes, amp_antes = espectro(senal_sucia, fs)
    frec_desp, amp_desp = espectro(senal_limpia, fs)

    frecuencias_medir = [17, 50, 150]
    print(f"{'Frecuencia [Hz]':<18} | {'Amp Antes':<15} | {'Amp Después':<15}")
    print("-" * 52)

    for f in frecuencias_medir:
        idx = np.argmin(np.abs(frec_antes - f))
        print(f"{f:<18.0f} | {amp_antes[idx]:<15.3f} | {amp_desp[idx]:<15.3f}")

    # 3. Error máximo (descartando transitorios)
    error = np.abs(senal_util[100:-100] - senal_limpia[100:-100])
    print(f"\nError máximo residual respecto a señal ideal: {np.max(error):.4f}")

    # 4. Análisis conceptual
    print("\n¿Por qué no usar un pasa-bajos con fc = 30 Hz?")
    print("Si la señal útil de un sensor abarcara componentes rápidas (ej. 0 a 100 Hz),")
    print("un pasa-bajos de 30 Hz distorsionaría severamente el pulso útil original.")


if __name__ == "__main__":
    main()