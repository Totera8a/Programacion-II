"""Módulo de diseño y aplicación de filtros pasa-bajos Butterworth."""

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
    """Aplica filtro para aislar la banda vocal y analiza atenuaciones."""
    fs = 16000.0
    t = np.arange(0, 0.5, 1 / fs)

    # Generación
    tonos_utiles = np.sin(2 * np.pi * 400 * t) + np.sin(2 * np.pi * 1000 * t) + np.sin(2 * np.pi * 3000 * t)
    interferencia = 0.8 * np.sin(2 * np.pi * 5500 * t)
    senal_original = tonos_utiles + interferencia

    # 1. Diseño del filtro
    f_corte = 3400.0
    b, a = signal.butter(6, f_corte, btype='lowpass', fs=fs)
    senal_filtrada = signal.filtfilt(b, a, senal_original)

    # 2. Análisis espectral antes y después
    frec_antes, amp_antes = espectro(senal_original, fs)
    frec_desp, amp_desp = espectro(senal_filtrada, fs)

    frecuencias_test = [400, 1000, 3000, 5500]
    print(f"{'Frecuencia':<12} | {'Amp Antes':<10} | {'Amp Desp':<10} | {'Atenuación [dB]':<15}")
    print("-" * 55)

    for f in frecuencias_test:
        idx = np.argmin(np.abs(frec_antes - f))
        a_in = amp_antes[idx]
        a_out = amp_desp[idx]
        atenuacion = 20 * np.log10(a_out / a_in)
        print(f"{f:<12} | {a_in:<10.3f} | {a_out:<10.3f} | {atenuacion:<15.2f}")

    # 3. Gráficos
    plt.figure(figsize=(12, 8))

    t_10ms = t <= 0.010
    plt.subplot(2, 2, 1)
    plt.plot(t[t_10ms] * 1000, senal_original[t_10ms], color='gray')
    plt.title("Señal Original (Temporal)")
    plt.ylabel("Amplitud")
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(t[t_10ms] * 1000, senal_filtrada[t_10ms], color='blue')
    plt.title("Señal Filtrada (Temporal)")
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(frec_antes, amp_antes, color='gray')
    plt.title("Espectro Original")
    plt.ylabel("Amplitud")
    plt.xlabel("Frecuencia [Hz]")
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(frec_desp, amp_desp, color='blue')
    plt.axvline(x=f_corte, color="red", linestyle=":", label="Corte (3400 Hz)")
    plt.title("Espectro Filtrado")
    plt.xlabel("Frecuencia [Hz]")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("El componente de 3000 Hz sí se atenúa levemente debido al 'roll-off' (caída gradual)")
    print("del filtro Butterworth, ya que 3000 Hz está cerca de la frecuencia de corte (3400 Hz).")


if __name__ == "__main__":
    main()