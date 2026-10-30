"""Módulo para el análisis y predicción de frecuencias aparentes por Aliasing."""

import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def frecuencia_aparente(f_real, fs):
    """Calcula la frecuencia aparente resultante del aliasing.

    Parámetros:
    f_real -- Frecuencia original de la señal en Hz.
    fs -- Frecuencia de muestreo en Hz.

    Retorna:
    Frecuencia resultante percibida tras muestreo en Hz.
    """
    return abs(f_real - fs * round(f_real / fs))


def main():
    """Evalúa matemática y empíricamente el fenómeno de submuestreo."""
    fs = 10000.0
    t = np.arange(0, 0.1, 1 / fs)
    frecuencias_reales_khz = [1, 3, 6, 7, 9, 11, 14]

    print(f"{'F. Real [kHz]':<15} | {'F. Fórmula [kHz]':<18} | {'F. Espectro [kHz]':<18}")
    print("-" * 55)

    for f_khz in frecuencias_reales_khz:
        f_real = f_khz * 1000.0
        tono = np.sin(2 * np.pi * f_real * t)
        
        f_formula = frecuencia_aparente(f_real, fs)
        
        frec, amp = espectro(tono, fs)
        f_espectro = frec[np.argmax(amp)]

        print(f"{f_khz:<15} | {f_formula/1000.0:<18.1f} | {f_espectro/1000.0:<18.1f}")

    f_max_lista = max(frecuencias_reales_khz) * 1000.0
    fs_requerida = 2 * f_max_lista
    print(f"\nMenor fs para representar correctamente 14 kHz: > {fs_requerida / 1000.0} kHz")


if __name__ == "__main__":
    main()