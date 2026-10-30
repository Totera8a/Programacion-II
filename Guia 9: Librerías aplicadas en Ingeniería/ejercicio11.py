"""Módulo de evaluación de disponibilidad de servicio y cumplimiento de SLA."""

import pandas as pd


def main():
    """Calcula el tiempo de actividad válido para cada enlace de la red."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Reportes esperados por estación (1 semana = 7 días * 96 reportes/día)
    reportes_esperados = 7 * 96

    # 2. Reportes válidos sin alarma (RSSI >= -75 dBm y no nulos)
    reportes_validos = df[(df["rssi"].notna()) & (df["rssi"] >= -75.0)].groupby("estacion").size()

    # 3. Disponibilidad porcentual
    disponibilidad = (reportes_validos / reportes_esperados) * 100.0

    # 4. Estaciones que incumplen SLA del 99%
    incumplen = disponibilidad[disponibilidad < 99.0].sort_values()

    print("--- Estaciones que no cumplen el SLA (99%) ---")
    print(incumplen.round(2))
    print("\nMotivos de incumplimiento:")
    print("El incumplimiento ocurre por la combinación de tres factores: huecos de pérdida de")
    print("comunicación (reportes faltantes), caídas físicas del enlace (datos de RSSI nulos)")
    print("y caídas de señal que superan el umbral operativo (alarmas de RSSI).")


if __name__ == "__main__":
    main()