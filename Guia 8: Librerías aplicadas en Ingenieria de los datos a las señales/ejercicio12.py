"""Módulo de demultiplexación de señales FDM mediante filtros pasa-banda."""

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


def extraer_canal(senal, f_central, ancho, fs):
    """Aplica un filtro pasa-banda Butterworth de orden 4 para aislar un canal.

    Parámetros:
    senal -- Señal multiplexada original.
    f_central -- Frecuencia central del canal en Hz.
    ancho -- Ancho de banda del canal en Hz.
    fs -- Frecuencia de muestreo.

    Retorna:
    Señal filtrada (ndarray).
    """
    f_baja = f_central - (ancho / 2)
    f_alta = f_central + (ancho / 2)
    b, a = signal.butter(4, [f_baja, f_alta], btype='bandpass', fs=fs)
    return signal.filtfilt(b, a, senal)


def main():
    """Genera señal FDM, extrae cada canal y grafica sus espectros."""
    fs = 16000.0
    t = np.arange(0, 0.5, 1 / fs)
    rng = np.random.default_rng(12)

    # Multiplexación de 4 canales
    canales_info = [(1000.0, 1.0), (2000.0, 0.7), (3000.0, 0.5), (4000.0, 0.3)]
    senal_fdm = np.zeros_like(t)
    for f, amp in canales_info:
        senal_fdm += amp * np.sin(2 * np.pi * f * t)
        
    senal_fdm += rng.normal(0, 0.2, len(t))

    plt.figure(figsize=(10, 12))

    # Espectro Original
    frec_orig, amp_orig = espectro(senal_fdm, fs)
    plt.subplot(5, 1, 1)
    plt.plot(frec_orig, amp_orig, color="black")
    plt.title("Espectro de la Señal Original (Multiplexada FDM)")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Extraer canales
    print(f"{'Canal [Hz]':<12} | {'Amp Original':<15} | {'Amp Recuperada'}")
    print("-" * 45)

    for i, (f_c, amp_teorica) in enumerate(canales_info):
        canal_filtrado = extraer_canal(senal_fdm, f_c, 400.0, fs)
        frec_c, amp_c = espectro(canal_filtrado, fs)
        
        idx = np.argmin(np.abs(frec_c - f_c))
        amp_recup = amp_c[idx]
        print(f"{f_c:<12.0f} | {amp_teorica:<15.2f} | {amp_recup:.3f}")

        # Análisis de rechazo de adyacentes para el canal 3000 Hz
        if f_c == 3000.0:
            print("\nRechazo de canales adyacentes en el filtro de 3000 Hz:")
            for f_adj, _ in canales_info:
                if f_adj != 3000.0:
                    idx_adj = np.argmin(np.abs(frec_c - f_adj))
                    amp_adj = amp_c[idx_adj]
                    rechazo_db = 20 * np.log10(amp_adj / amp_recup) if amp_adj > 0 else -100
                    print(f" -> Quedan {rechazo_db:.1f} dB de la señal de {f_adj:.0f} Hz")
            print()

        # Gráficos de canales individuales
        plt.subplot(5, 1, i + 2)
        plt.plot(frec_c, amp_c, color="blue")
        plt.title(f"Espectro del Canal {f_c:.0f} Hz Extraído")
        plt.ylabel("Amplitud")
        plt.grid(True)

    plt.xlabel("Frecuencia [Hz]")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()