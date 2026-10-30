"""Módulo de evaluación de resolución frecuencial de la FFT."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def main():
    """Analiza cómo la ventana de observación temporal afecta la resolución espectral."""
    fs = 1000.0
    duraciones = [0.25, 0.5, 1.0, 2.0]

    plt.figure(figsize=(10, 8))

    for i, duracion in enumerate(duraciones):
        t = np.arange(0, duracion, 1 / fs)
        resolucion = fs / len(t)
        
        tono_doble = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 102 * t)
        frec, amp = espectro(tono_doble, fs)

        # Encontrar picos entre 95 y 107 Hz con amp > 0.5
        mask = (frec >= 95) & (frec <= 107) & (amp > 0.5)
        picos_detectados = frec[mask]

        print(f"Duración: {duracion}s | Resolución: {resolucion:.1f} Hz | Picos detectados: {picos_detectados}")

        # Gráficos
        mask_grafico = (frec >= 90) & (frec <= 112)
        plt.subplot(2, 2, i + 1)
        plt.plot(frec[mask_grafico], amp[mask_grafico], marker='o')
        plt.title(f"Duración {duracion}s (Res = {resolucion} Hz)")
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("Amplitud")
        plt.grid(True)

    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("Para 0.25s la resolución es de 4 Hz, por lo que el FFT mezcla 100 y 102 Hz en un solo lóbulo.")
    print("Ambas frecuencias logran separarse correctamente a partir de una duración de 1 segundo (resolución 1 Hz).")


if __name__ == "__main__":
    main()