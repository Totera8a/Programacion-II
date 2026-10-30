"""Módulo para el rastreo y detección de frecuencias y amplitudes ciegas."""

import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def senal_misteriosa(t, semilla):
    """Tres portadoras de frecuencia y amplitud desconocidas, más ruido (Cátedra)."""
    rng = np.random.default_rng(semilla)
    frecuencias = rng.choice(np.arange(500, 4500, 10), 3, replace=False)
    amplitudes = rng.uniform(0.3, 1.0, 3)
    senal = np.zeros(len(t))
    
    for f, a in zip(frecuencias, amplitudes):
        senal += a * np.sin(2 * np.pi * f * t)
        
    # Variables internas expuestas solo para validación visual al final
    return senal + rng.normal(0, 0.8, len(t)), frecuencias, amplitudes


def detector_ciego(t, fs, semilla):
    """Analiza la señal misteriosa y extrae las portadoras detectadas."""
    senal, f_reales, a_reales = senal_misteriosa(t, semilla)
    frec, amp = espectro(senal, fs)

    # Calcular piso de ruido y umbral
    piso_ruido = np.median(amp)
    umbral = 10 * piso_ruido

    # Extraer picos que superan el umbral
    mask_deteccion = amp > umbral
    f_detectadas = frec[mask_deteccion]
    a_detectadas = amp[mask_deteccion]

    print(f"\n--- Análisis de Semilla {semilla} ---")
    print(f"Umbral automático fijado en: {umbral:.3f}")
    
    print("Valores Detectados:")
    for f_det, a_det in zip(f_detectadas, a_detectadas):
        print(f" -> Frec: {f_det:4.0f} Hz | Amp: {a_det:.3f}")
        
    print("Valores Reales (Validación Interna):")
    for f_real, a_real in zip(f_reales, a_reales):
        print(f" -> Frec: {f_real:4.0f} Hz | Amp: {a_real:.3f}")


def main():
    """Ejecuta el detector sobre múltiples configuraciones de ruido y frecuencias."""
    fs = 10000.0
    t = np.arange(0, 1.0, 1 / fs)

    for semilla in [1, 2, 3]:
        detector_ciego(t, fs, semilla)


if __name__ == "__main__":
    main()