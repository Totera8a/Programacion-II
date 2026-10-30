"""Módulo de análisis del comportamiento diurno y ciclos de temperatura/señal."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def promedio_potencia_dbm(serie_rssi):
    """Calcula el promedio cuadrático en potencia y lo reconvierte a dBm."""
    serie_valida = serie_rssi.dropna()
    potencia_mw = 10 ** (serie_valida / 10)
    return 10 * np.log10(potencia_mw.mean())


def main():
    """Grafica los perfiles horarios de temperatura y RSSI de la red."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    df["hora"] = df["timestamp"].dt.hour

    # 1. Agrupación por hora
    temp_horaria = df.groupby("hora")["temperatura"].mean()
    rssi_horario = df.groupby("hora")["rssi"].apply(promedio_potencia_dbm)

    # 2. Gráficos
    horas = np.arange(24)
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(horas, temp_horaria, color="crimson", marker="o", linewidth=2)
    plt.title("Perfil Horario de Temperatura Promedio en la Red")
    plt.ylabel("Temperatura [°C]")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(horas, rssi_horario, color="royalblue", marker="s", linewidth=2)
    plt.title("Perfil Horario de RSSI Promedio en Potencia")
    plt.xlabel("Hora del Día [0 - 23 hs]")
    plt.ylabel("RSSI [dBm]")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # 3. Diagnóstico de valores extremos
    hora_caliente = temp_horaria.idxmax()
    hora_fria = temp_horaria.idxmin()
    dif_temp = temp_horaria.max() - temp_horaria.min()

    print(f"Hora más caliente: {hora_caliente}:00 hs ({temp_horaria.max():.2f} °C)")
    print(f"Hora más fría: {hora_fria}:00 hs ({temp_horaria.min():.2f} °C)")
    print(f"Amplitud térmica diaria promedio: {dif_temp:.2f} °C")


if __name__ == "__main__":
    main()