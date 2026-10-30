"""Módulo para el análisis del inventario y características fijas de la red."""

import pandas as pd

VELOCIDAD_LUZ = 299792458  # m/s


def main():
    """Genera el inventario de estaciones y calcula longitudes de onda."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Tabla con una fila por estación
    inventario = df.groupby("estacion")[["frecuencia", "potencia"]].first()

    # 2. Comprobar constantes
    variaciones = df.groupby("estacion")[["frecuencia", "potencia"]].nunique()
    cambios = (variaciones > 1).any().any()
    print(f"¿Alguna estación cambió de frecuencia o potencia?: {cambios}")

    # 3. Estaciones por banda y potencia promedio
    conteo_bandas = inventario.groupby("frecuencia").size()
    pot_promedio_banda = inventario.groupby("frecuencia")["potencia"].mean()

    print("\n--- Estaciones por Banda de Frecuencia [MHz] ---")
    for banda, cantidad in conteo_bandas.items():
        print(f"Banda {banda} MHz: {cantidad} estaciones | Potencia promedio: {pot_promedio_banda[banda]:.1f} dBm")

    # 4. Longitud de onda en cm (lambda = c / f)
    inventario["longitud_onda_cm"] = (VELOCIDAD_LUZ / (inventario["frecuencia"] * 1e6)) * 100
    print("\n--- Inventario Completo ---")
    print(inventario)


if __name__ == "__main__":
    main()