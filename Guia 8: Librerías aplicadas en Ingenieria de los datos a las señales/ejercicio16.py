"""Módulo de estudio espectral del filtro de promedio móvil (Moving Average)."""

import matplotlib.pyplot as plt
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
    """Evalúa la respuesta frecuencial de un promedio móvil como filtro."""
    fs = 1000.0
    t = np.arange(0, 1.0, 1 / fs)
    rng = np.random.default_rng(42)

    senal = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 250 * t) + rng.normal(0, 0.3, len(t))

    # 1. Comparación con pasa-bajos
    N = 10
    senal_ma = np.convolve(senal, np.ones(N) / N, mode="same")
    
    b_butter, a_butter = signal.butter(4, 150, btype='lowpass', fs=fs)
    senal_butter = signal.filtfilt(b_butter, a_butter, senal)

    frec, amp_ma = espectro(senal_ma, fs)
    _, amp_butter = espectro(senal_butter, fs)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(frec, amp_butter, label="Butterworth (150 Hz)", alpha=0.7)
    plt.plot(frec, amp_ma, label="Promedio Móvil (N=10)", alpha=0.7)
    plt.title("Espectro Resultante de Señal Filtrada")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True)

    # 2. Respuesta en frecuencia del promedio móvil para distintos N
    plt.subplot(1, 2, 2)
    for n_val in [5, 10, 20]:
        b_ma = np.ones(n_val) / n_val
        w, h = signal.freqz(b_ma, [1], worN=4000, fs=fs)
        # Evitar logaritmo de cero con np.maximum
        atenuacion_db = 20 * np.log10(np.maximum(np.abs(h), 1e-5))
        plt.plot(w, atenuacion_db, label=f"N = {n_val}")

    plt.title("Respuesta en Frecuencia (Promedio Móvil)")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Ganancia [dB]")
    plt.ylim(-40, 5)
    plt.xlim(0, 500)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print("--- Ventajas y Desventajas del Promedio Móvil ---")
    print("Ventajas: Extremadamente rápido y computacionalmente barato en hardware y software.")
    print("Desventajas: Pobre caída de rechazo (roll-off), no atenúa uniformemente las altas frecuencias")
    print("y presenta picos de rebote (lóbulos laterales) que dejan pasar ruido indeseado.")


if __name__ == "__main__":
    main()