"""Módulo de optimización de la ubicación de un repetidor para maximizar el margen."""

import matplotlib.pyplot as plt
import numpy as np

VELOCIDAD_LUZ = 299792458
DISTANCIA_TOTAL_KM = 30.0
FRECUENCIA_HZ = 5.8e9
P_TX_DBM = 23.0
G_ANT_DBI = 20.0
UMBRAL_DBM = -75.0


def calcular_margen(distancia_km):
    """Calcula el margen de un tramo en dB.

    Parámetros:
    distancia_km -- Distancia del tramo en kilómetros.

    Retorna:
    Margen en dB (float/ndarray).
    """
    distancia_m = distancia_km * 1000.0
    fspl = 20 * np.log10((4 * np.pi * distancia_m * FRECUENCIA_HZ) / VELOCIDAD_LUZ)
    p_rx = P_TX_DBM + (2 * G_ANT_DBI) - fspl
    return p_rx - UMBRAL_DBM


def main():
    """Compara enlace directo de 30 km con enlace usando repetidor intermedio."""
    # 1. Enlace directo
    margen_directo = calcular_margen(DISTANCIA_TOTAL_KM)

    # 2. Enlace con repetidor
    x_km = np.linspace(1.0, 29.0, 500)
    margen_tramo1 = calcular_margen(x_km)
    margen_tramo2 = calcular_margen(DISTANCIA_TOTAL_KM - x_km)
    margen_total = np.minimum(margen_tramo1, margen_tramo2)

    # 3. Ubicación óptima
    idx_opt = np.argmax(margen_total)
    x_optimo = x_km[idx_opt]
    margen_max = margen_total[idx_opt]

    print(f"Margen del enlace directo: {margen_directo:.2f} dB")
    print(f"Ubicación óptima del repetidor: {x_optimo:.2f} km")
    print(f"Margen del enlace con repetidor: {margen_max:.2f} dB")

    # 4. Gráfico
    plt.figure(figsize=(9, 5))
    plt.plot(x_km, margen_total, label="Margen con Repetidor", color="purple", linewidth=2)
    plt.axhline(y=margen_directo, color="red", linestyle="--", label="Margen Enlace Directo")
    plt.axvline(x=x_optimo, color="green", linestyle=":", label=f"Ubicación Óptima ({x_optimo:.1f} km)")

    plt.title("Margen de Enlace vs. Ubicación del Repetidor")
    plt.xlabel("Distancia del punto inicial al repetidor [km]")
    plt.ylabel("Margen de Enlace [dB]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Justificación ---")
    print("Es esperable que convenga situarlo exactamente a la mitad (15 km) porque el FSPL no es lineal;")
    print("al equidistar de ambos extremos se balancean las pérdidas de los dos tramos.")


if __name__ == "__main__":
    main()