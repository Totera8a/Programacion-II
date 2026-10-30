"""Módulo de análisis de variabilidad e histogramas de señal para dos estaciones."""

import matplotlib.pyplot as plt
import numpy as np

UMBRAL_DBM = -75.0


def main():
    """Compara métricas de desempeño e histogramas entre dos estaciones."""
    rng = np.random.default_rng(14)
    e01 = rng.normal(-66.0, 2.0, 2000)
    e02 = rng.normal(-64.0, 6.0, 2000)

    # Cálculos para E01
    prom_e01 = 10 * np.log10(np.mean(10 ** (e01 / 10)))
    std_e01 = np.std(e01)
    pct_bajo_e01 = np.mean(e01 < UMBRAL_DBM) * 100.0

    # Cálculos para E02
    prom_e02 = 10 * np.log10(np.mean(10 ** (e02 / 10)))
    std_e02 = np.std(e02)
    pct_bajo_e02 = np.mean(e02 < UMBRAL_DBM) * 100.0

    print(f"E01 -> Promedio: {prom_e01:.2f} dBm | Desvío: {std_e01:.2f} dB | % Falla: {pct_bajo_e01:.2f}%")
    print(f"E02 -> Promedio: {prom_e02:.2f} dBm | Desvío: {std_e02:.2f} dB | % Falla: {pct_bajo_e02:.2f}%")

    # Histogramas
    plt.figure(figsize=(9, 5))
    plt.hist(e01, bins=40, alpha=0.5, label="E01 (std=2 dB)", color="blue")
    plt.hist(e02, bins=40, alpha=0.5, label="E02 (std=6 dB)", color="orange")
    plt.axvline(x=UMBRAL_DBM, color="red", linestyle="--", label="Umbral (-75 dBm)")

    plt.title("Estabilidad de señal: Histograma RSSI E01 vs E02")
    plt.xlabel("RSSI [dBm]")
    plt.ylabel("Frecuencia de muestras")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("E01 es mejor estación. Aunque E02 tiene mejor promedio, su alta variabilidad (std=6 dB)")
    print("provoca caídas frecuentes por debajo del umbral operativo.")


if __name__ == "__main__":
    main()