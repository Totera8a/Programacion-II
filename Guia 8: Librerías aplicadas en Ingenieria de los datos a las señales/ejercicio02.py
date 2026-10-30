"""Módulo para la inyección de ruido Gaussiano controlado por SNR."""

import matplotlib.pyplot as plt
import numpy as np


def sigma_para_snr(senal, snr_db):
    """Calcula la desviación estándar del ruido requerida para una SNR objetivo.

    Parámetros:
    senal -- Vector NumPy de la señal original.
    snr_db -- Relación señal a ruido deseada en decibelios.

    Retorna:
    Desviación estándar del ruido (float).
    """
    potencia_senal = np.mean(senal ** 2)
    potencia_ruido = potencia_senal / (10 ** (snr_db / 10))
    return np.sqrt(potencia_ruido)


def calcular_snr_db(senal, ruido):
    """Calcula la SNR resultante de una señal y su ruido aditivo."""
    pot_senal = np.mean(senal ** 2)
    pot_ruido = np.mean(ruido ** 2)
    return 10 * np.log10(pot_senal / pot_ruido)


def main():
    """Genera tonos contaminados con diferentes niveles de SNR."""
    fs = 8000.0
    t = np.arange(0, 1.0, 1 / fs)
    tono = np.sin(2 * np.pi * 1000 * t)
    rng = np.random.default_rng(2)

    snrs_objetivo = [20, 10, 0, -5]
    
    plt.figure(figsize=(10, 8))

    for i, snr in enumerate(snrs_objetivo):
        sigma = sigma_para_snr(tono, snr)
        ruido = rng.normal(0, sigma, len(t))
        senal_ruidosa = tono + ruido
        
        snr_medida = calcular_snr_db(tono, ruido)
        print(f"Objetivo: {snr:2d} dB -> Medida: {snr_medida:5.2f} dB (Sigma: {sigma:.3f})")

        # Graficar primeros 5 ms
        plt.subplot(2, 2, i + 1)
        mascara_5ms = t <= 0.005
        plt.plot(t[mascara_5ms] * 1000, senal_ruidosa[mascara_5ms], label=f"SNR={snr}dB")
        plt.plot(t[mascara_5ms] * 1000, tono[mascara_5ms], color="red", linestyle="--", alpha=0.5)
        plt.title(f"Señal con SNR {snr} dB")
        plt.xlabel("Tiempo [ms]")
        plt.ylabel("Amplitud")
        plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()