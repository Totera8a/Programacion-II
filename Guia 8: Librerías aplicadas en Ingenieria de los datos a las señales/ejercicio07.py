"""Módulo de demostración de sumas armónicas de Fourier para ondas cuadradas."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def onda_cuadrada(t, f0, cantidad_armonicos):
    """Genera una onda cuadrada mediante suma de series de Fourier.

    Parámetros:
    t -- Vector de tiempos.
    f0 -- Frecuencia fundamental en Hz.
    cantidad_armonicos -- Cantidad de armónicos impares a sumar.

    Retorna:
    Vector NumPy con la amplitud de la onda.
    """
    senal = np.zeros_like(t)
    for i in range(cantidad_armonicos):
        k = 2 * i + 1  # 1, 3, 5, 7...
        senal += (4 / (np.pi * k)) * np.sin(2 * np.pi * k * f0 * t)
    return senal


def main():
    """Genera aproximaciones de ondas cuadradas y verifica sus componentes."""
    fs = 20000.0
    f0 = 100.0
    t = np.arange(0, 0.04, 1 / fs)

    armonicos = [1, 3, 10, 50]
    
    plt.figure(figsize=(10, 6))

    for k in armonicos:
        cuadrada = onda_cuadrada(t, f0, k)
        plt.plot(t[t <= 0.02] * 1000, cuadrada[t <= 0.02], label=f"{k} armónicos")

    plt.title("Construcción de Onda Cuadrada (Series de Fourier)")
    plt.xlabel("Tiempo [ms]")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Análisis del espectro para 10 armónicos
    cuadrada_10 = onda_cuadrada(t, f0, 10)
    frec, amp = espectro(cuadrada_10, fs)
    
    # Filtrar solo donde hay picos significativos
    picos_mask = amp > 0.05
    frec_picos = frec[picos_mask]
    amp_picos = amp[picos_mask]

    print("\nComprobación de espectro para 10 armónicos:")
    print(f"{'Frecuencia [Hz]':<18} | {'Amplitud Espectro':<20} | {'Amplitud Teórica 4/(pi*k)':<20}")
    print("-" * 65)

    for i, f_pico in enumerate(frec_picos):
        k = f_pico / f0
        amp_teorica = 4 / (np.pi * k)
        print(f"{f_pico:<18.1f} | {amp_picos[i]:<20.4f} | {amp_teorica:<20.4f}")


if __name__ == "__main__":
    main()