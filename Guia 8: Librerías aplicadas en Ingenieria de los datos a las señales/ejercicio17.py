"""Módulo de evaluación de mejora de relación señal a ruido mediante filtrado."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def calcular_snr_db(pot_senal, pot_ruido):
    """Calcula la SNR en dB dadas las potencias absolutas."""
    return 10 * np.log10(pot_senal / pot_ruido)


def main():
    """Analiza empíricamente cómo el estrechamiento del filtro impacta en la SNR."""
    fs = 1000.0
    t = np.arange(0, 2.0, 1 / fs)
    rng = np.random.default_rng(17)

    tono = 1.0 * np.sin(2 * np.pi * 100 * t)
    ruido = rng.normal(0, 1.5, len(t))

    # 1. SNR Original
    pot_tono_in = np.mean(tono ** 2)
    pot_ruido_in = np.mean(ruido ** 2)
    snr_original = calcular_snr_db(pot_tono_in, pot_ruido_in)

    print(f"SNR Original sin filtrar: {snr_original:.2f} dB")
    print(f"{'Ancho Banda [Hz]':<18} | {'SNR Filtrada [dB]':<18} | {'Mejora SNR [dB]':<18}")
    print("-" * 58)

    anchos = [100.0, 40.0, 20.0, 10.0]
    mejoras = []

    # 2. y 3. Filtrado y medición
    for bw in anchos:
        f_baja = 100.0 - (bw / 2)
        f_alta = 100.0 + (bw / 2)
        b, a = signal.butter(4, [f_baja, f_alta], btype='bandpass', fs=fs)

        tono_filtrado = signal.filtfilt(b, a, tono)
        ruido_filtrado = signal.filtfilt(b, a, ruido)

        pot_tono_out = np.mean(tono_filtrado ** 2)
        pot_ruido_out = np.mean(ruido_filtrado ** 2)
        
        snr_out = calcular_snr_db(pot_tono_out, pot_ruido_out)
        mejora = snr_out - snr_original
        mejoras.append(mejora)
        
        print(f"{bw:<18.0f} | {snr_out:<18.2f} | {mejora:<18.2f}")

    # 4. Gráfico
    plt.figure(figsize=(7, 4))
    plt.plot(anchos, mejoras, marker="o", color="blue", linewidth=2)
    plt.gca().invert_xaxis()  # Invertir eje para ver cómo al 'achicar' sube la mejora
    plt.title("Mejora de SNR vs. Ancho de Banda del Filtro")
    plt.xlabel("Ancho de Banda del Filtro Pasa-Banda [Hz]")
    plt.ylabel("Mejora de SNR [dB]")
    plt.grid(True)
    plt.show()

    print("\n--- Relación Conceptual ---")
    print("Dividir el ancho de banda por 10 (ej. de 100 a 10 Hz) mejora la SNR en ~10 dB.")
    print("Esto se debe a que la potencia del piso de ruido térmico (kTB) es directamente")
    print("proporcional al ancho de banda B; si B se reduce linealmente, el ruido cae en igual proporción.")


if __name__ == "__main__":
    main()