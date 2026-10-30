"""Módulo de clasificación categórica de niveles de RSSI."""

import numpy as np
import pandas as pd


def main():
    """Clasifica cada medición según rangos de calidad operacional."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Clasificación con np.select
    condiciones = [
        df["rssi"] > -60.0,
        (df["rssi"] >= -67.0) & (df["rssi"] <= -60.0),
        (df["rssi"] > -75.0) & (df["rssi"] < -67.0),
        df["rssi"] <= -75.0,
    ]
    categorias = ["Excelente", "Buena", "Regular", "Mala"]
    df["calidad"] = np.select(condiciones, categorias, default=np.nan)

    # 2. Conteo global y porcentajes
    conteo = df["calidad"].value_counts(dropna=False)
    porcentajes = df["calidad"].value_counts(normalize=True, dropna=False) * 100

    print("--- Distribución de Calidad de Señal en la Red ---")
    for cat in categorias:
        print(f"Categoría {cat:<10}: {conteo[cat]:5d} muestras ({porcentajes[cat]:6.2f}%)")

    # 3. Porcentaje 'Excelente' por estación (ordenado)
    excelente_por_estacion = (
        df[df["calidad"] == "Excelente"].groupby("estacion").size() / df.groupby("estacion").size()
    ) * 100
    excelente_ordenado = excelente_por_estacion.fillna(0).sort_values(ascending=False)

    print("\n--- Porcentaje de Calidad 'Excelente' por Estación ---")
    print(np.round(excelente_ordenado, 2))

    # 4. Verificación de alarmas de RSSI
    alarmas_rssi = (df["rssi"] <= -75.0).sum()
    mediciones_malas = (df["calidad"] == "Mala").sum()
    print(f"\n¿Coincide la cantidad de mediciones 'Mala' ({mediciones_malas}) con las alarmas ({alarmas_rssi})?: {alarmas_rssi == mediciones_malas}")


if __name__ == "__main__":
    main()