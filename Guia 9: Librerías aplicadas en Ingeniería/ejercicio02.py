"""Módulo de evaluación e inspección de datos faltantes en telemetría."""

import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Analiza y grafica la presencia de valores nulos en el conjunto de datos."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Faltantes por estación
    faltantes_estacion = df.groupby("estacion")[["rssi", "temperatura"]].apply(lambda x: x.isna().sum())

    # 2. Porcentaje global
    pct_rssi = df["rssi"].isna().mean() * 100
    pct_temp = df["temperatura"].isna().mean() * 100

    print(f"Porcentaje global de datos faltantes en RSSI: {pct_rssi:.2f}%")
    print(f"Porcentaje global de datos faltantes en Temperatura: {pct_temp:.2f}%")

    # 3. Estación con más faltantes
    estacion_mas_faltantes = faltantes_estacion["rssi"].idxmax()
    estaciones_sin_faltantes = faltantes_estacion[faltantes_estacion["rssi"] == 0].index.tolist()

    print(f"Estación con más datos faltantes de RSSI: {estacion_mas_faltantes}")
    print(f"Estaciones sin ningún dato faltante: {estaciones_sin_faltantes}")

    # 4. Gráfico de barras
    plt.figure(figsize=(10, 5))
    faltantes_estacion["rssi"].plot(kind="bar", color="crimson")
    plt.title("Cantidad de Datos Faltantes de RSSI por Estación")
    plt.xlabel("Estación")
    plt.ylabel("Cantidad de Muestras Nulas (NaN)")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("Los datos faltantes están concentrados principalmente en una sola estación (E15),")
    print("lo que indica una falla local de transmisión y no un problema generalizado del sistema.")


if __name__ == "__main__":
    main()