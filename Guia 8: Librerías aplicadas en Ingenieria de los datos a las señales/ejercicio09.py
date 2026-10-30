"""Módulo de análisis de bandas laterales en transmisiones AM."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def generar_am(t, fc, fm, m):
    """Genera una señal modulada en amplitud.

    Parámetros:
    t -- Vector de tiempos.
    fc -- Frecuencia de portadora en Hz.
    fm -- Frecuencia del mensaje en Hz.
    m -- Índice de modulación.

    Retorna:
    Vector de la señal AM.
    """
    envolvente = 1 + (m * np.cos(2 * np.pi * fm * t))
    portadora = np.cos(2 * np.pi * fc * t)
    return envolvente * portadora, envolvente


def main():
    """Analiza la portadora y bandas laterales según el índice de modulación."""
    fs = 10000.0
    fc = 1000.0
    fm = 50.0
    t = np.arange(0, 1.0, 1 / fs)

    # Gráfico temporal para m=0.5
    am_05, env_05 = generar_am(t, fc, fm, 0.5)
    t_60ms = t <= 0.06

    plt.figure(figsize=(10, 4))
    plt.plot(t[t_60ms] * 1000, am_05[t_60ms], label="Señal AM")
    plt.plot(t[t_60ms] * 1000, env_05[t_60ms], label="Envolvente (+)", color="red", linestyle="--")
    plt.plot(t[t_60ms] * 1000, -env_05[t_60ms], label="Envolvente (-)", color="red", linestyle="--")
    plt.title("Modulación AM (m = 0.5)")
    plt.xlabel("Tiempo [ms]")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Análisis espectral para diferentes índices
    indices = [0.5, 1.0, 0.2]
    print(f"{'Índice m':<10} | {'Freq Portadora':<16} | {'Amp Portadora':<15} | {'Freq Lat':<12} | {'Amp Lat (Teórica: m/2)'}")
    print("-" * 80)

    for m in indices:
        senal, _ = generar_am(t, fc, fm, m)
        frec, amp = espectro(senal, fs)
        
        mask_picos = amp > 0.05
        frec_p = frec[mask_picos]
        amp_p = amp[mask_picos]

        f_port = frec_p[1]
        amp_port = amp_p[1]
        f_lat = frec_p[2]
        amp_lat = amp_p[2]

        print(f"{m:<10} | {f_port:<16.1f} | {amp_port:<15.3f} | {f_lat:<12.1f} | {amp_lat:.3f} ({m/2:.3f})")


if __name__ == "__main__":
    main()