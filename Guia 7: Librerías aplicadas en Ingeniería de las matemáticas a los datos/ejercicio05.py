"""Módulo para graficar curvas de potencia recibida en función de la distancia."""

import matplotlib.pyplot as plt
import numpy as np

VELOCIDAD_LUZ = 299792458
P_TX_DBM = 23.0
G_ANT_DBI = 15.0
UMBRAL_DBM = -75.0


def main():
    """Genera gráfico comparativo de alcance para 2.4 GHz y 5.8 GHz."""
    distancias_km = np.linspace(0.5, 40.0, 1000)
    distancias_m = distancias_km * 1000.0

    # Pérdida y potencia recibida
    fspl_24 = 20 * np.log10((4 * np.pi * distancias_m * 2.4e9) / VELOCIDAD_LUZ)
    p_rx_24 = P_TX_DBM + (2 * G_ANT_DBI) - fspl_24

    fspl_58 = 20 * np.log10((4 * np.pi * distancias_m * 5.8e9) / VELOCIDAD_LUZ)
    p_rx_58 = P_TX_DBM + (2 * G_ANT_DBI) - fspl_58

    # Alcance máximo usando máscaras de NumPy
    alcance_24 = distancias_km[np.where(p_rx_24 >= UMBRAL_DBM)[0][-1]]
    alcance_58 = distancias_km[np.where(p_rx_58 >= UMBRAL_DBM)[0][-1]]

    print(f"Alcance máximo en 2.4 GHz: {alcance_24:.2f} km")
    print(f"Alcance máximo en 5.8 GHz: {alcance_58:.2f} km")

    # Configuración del gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(distancias_km, p_rx_24, label="2.4 GHz", color="blue", linewidth=2)
    plt.plot(distancias_km, p_rx_58, label="5.8 GHz", color="orange", linewidth=2)
    plt.axhline(y=UMBRAL_DBM, color="red", linestyle="--", label="Umbral (-75 dBm)")

    plt.axvline(x=alcance_24, color="blue", linestyle=":", label=f"Alcance Max 2.4 GHz ({alcance_24:.1f} km)")
    plt.axvline(x=alcance_58, color="orange", linestyle=":", label=f"Alcance Max 5.8 GHz ({alcance_58:.1f} km)")

    plt.title("Potencia Recibida vs. Distancia")
    plt.xlabel("Distancia [km]")
    plt.ylabel("Potencia Recibida [dBm]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()