"""Módulo de análisis multidimensional de telemetría de red con NumPy."""

import numpy as np


def main():
    """Procesa una matriz 5x24 de mediciones de RSSI simuladas."""
    rng = np.random.default_rng(12)
    matriz_rssi = rng.normal(-70.0, 3.0, (5, 24))

    # Caída agregada a la estación 3 (índice 2) entre 10h y 15h
    matriz_rssi[2, 10:16] -= 8.0

    # 1. Promedio en potencia por estación
    matriz_mw = 10 ** (matriz_rssi / 10)
    promedios_dbm = 10 * np.log10(np.mean(matriz_mw, axis=1))

    # 2. Hora del peor RSSI
    peor_hora = np.argmin(matriz_rssi, axis=1)

    # 3. Horas con alguna estación en alarma (< -75 dBm)
    horas_alarma = np.where(np.any(matriz_rssi < -75.0, axis=0))[0]

    # 4. Estación con más horas en alarma
    alarmas_por_estacion = np.sum(matriz_rssi < -75.0, axis=1)
    estacion_peor = np.argmax(alarmas_por_estacion) + 1

    print("Promedio en potencia por estación [dBm]:", np.round(promedios_dbm, 2))
    print("Hora de peor RSSI por estación:", peor_hora)
    print("Horas con al menos una alarma (< -75 dBm):", horas_alarma)
    print(f"Estación con más horas en alarma: Estación E0{estacion_peor} ({alarmas_por_estacion[estacion_peor - 1]} hs)")


if __name__ == "__main__":
    main()