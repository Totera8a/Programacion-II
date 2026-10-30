"""Módulo de generación de informes diarios consolidados de telemetría."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def promedio_potencia_dbm(serie_rssi):
    """Calcula el promedio cuadrático en potencia en dBm."""
    serie_valida = serie_rssi.dropna()
    potencia_mw = 10 ** (serie_valida / 10)
    return 10 * np.log10(potencia_mw.mean())


def main():
    """Sintetiza la actividad diaria e identifica fechas críticas de fallas."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    df["fecha"] = df["timestamp"].dt.date

    # Agrupación por día
    resumen = df.groupby("fecha").agg(
        rssi_prom_dbm=("rssi", promedio_potencia_dbm),
        temp_max=("temperatura", "max"),
        alarmas_rssi=("rssi", lambda x: (x < -75.0).sum()),
        alarmas_temp=("temperatura", lambda x: (x > 60.0).sum()),
        reportes_recibidos=("timestamp", "count"),
    )

    print("--- Resumen Diario de la Red ---")
    print(resumen)

    # Gráfico de alarmas por día
    plt.figure(figsize=(9, 4))
    resumen["alarmas_rssi"].plot(kind="bar", color="darkorange")
    plt.title("Cantidad de Alarmas de RSSI (< -75 dBm) por Día")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de Alarmas")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()