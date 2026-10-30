"""Módulo de evaluación de correlación entre temperatura y potencia recibida."""

import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Calcula coeficientes de correlación de Pearson y grafica dispersión."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Correlación global
    corr_global = df["rssi"].corr(df["temperatura"])
    print(f"Correlación global RSSI vs. Temperatura: {corr_global:.4f}")

    # 2. Correlación por estación
    corr_estaciones = df.groupby("estacion").apply(lambda g: g["rssi"].corr(g["temperatura"]))
    print("\n--- Correlación por Estación (Ordenada) ---")
    print(corr_estaciones.sort_values())

    # 3. Gráfico de dispersión para la estación de mayor correlación absoluta
    est_max_corr = corr_estaciones.abs().idxmax()
    df_est = df[df["estacion"] == est_max_corr]

    plt.figure(figsize=(8, 5))
    plt.scatter(df_est["temperatura"], df_est["rssi"], alpha=0.5, color="purple")
    plt.title(f"Diagrama de Dispersión RSSI vs. Temp ({est_max_corr})")
    plt.xlabel("Temperatura [°C]")
    plt.ylabel("RSSI [dBm]")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()