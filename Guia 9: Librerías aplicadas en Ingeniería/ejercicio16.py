"""Módulo de evaluación estadística agrupadora de bandas de transmisión."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def promedio_potencia_dbm(serie):
    """Calcula el promedio en potencia en dBm."""
    mw = 10 ** (serie.dropna() / 10)
    return 10 * np.log10(mw.mean())


def main():
    """Genera métricas consolidadas y diagramas de caja para cada banda."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    df["banda"] = df["frecuencia"]

    # 1. Agrupamiento por banda
    metricas = df.groupby("banda").agg(
        rssi_promedio=("rssi", promedio_potencia_dbm),
        desvio_rssi=("rssi", "std"),
        alarmas=("rssi", lambda x: (x < -75.0).sum())
    )
    
    print("--- Desempeño Consolidado por Banda de Frecuencia ---")
    print(np.round(metricas, 2))

    # 2. Preparar datos para el Boxplot
    df_clean = df.dropna(subset=["rssi"])
    bandas_unicas = sorted(df_clean["banda"].unique())
    datos_grafico = [df_clean[df_clean["banda"] == b]["rssi"].values for b in bandas_unicas]

    # Gráfico Boxplot
    plt.figure(figsize=(9, 6))
    plt.boxplot(datos_grafico, labels=[f"{b} MHz" for b in bandas_unicas])
    plt.title("Distribución de RSSI por Banda de Operación")
    plt.ylabel("RSSI [dBm]")
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.show()

    # 3. Interpretación del gráfico
    print("\n--- Interpretación del Boxplot ---")
    print("- La caja: Representa el 50% central de los datos (Rango Intercuartílico).")
    print("- La línea central: Es la mediana de la distribución.")
    print("- Los puntos sueltos: Son valores atípicos (outliers). Suelen pertenecer")
    print("  a estaciones defectuosas específicas (como la detectada en degradación profunda).")


if __name__ == "__main__":
    main()