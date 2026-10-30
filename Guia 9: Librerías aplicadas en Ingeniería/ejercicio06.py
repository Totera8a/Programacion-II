"""Módulo para estimar pérdida de trayecto y distancia equivalente en espacio libre."""

import numpy as np
import pandas as pd

VELOCIDAD_LUZ = 299792458  # m/s


def promedio_potencia_dbm(serie_rssi):
    """Calcula el promedio en potencia de una serie de RSSI."""
    serie_valida = serie_rssi.dropna()
    potencia_mw = 10 ** (serie_valida / 10)
    return 10 * np.log10(potencia_mw.mean())


def main():
    """Calcula pérdidas de trayecto y distancias equivalentes de cada enlace."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    info_est = df.groupby("estacion")[["frecuencia", "potencia"]].first()
    rssi_prom = df.groupby("estacion")["rssi"].apply(promedio_potencia_dbm)

    tabla = info_est.copy()
    tabla["rssi_promedio"] = rssi_prom

    # L_trayecto = Ptx + Gtx + Grx - RSSI_prom
    tabla["l_trayecto_db"] = tabla["potencia"] + 2.0 + 2.0 - tabla["rssi_promedio"]

    # d_eq [km] = (c / (4 * pi * f_hz)) * 10^(L / 20) / 1000
    f_hz = tabla["frecuencia"] * 1e6
    tabla["d_equivalente_km"] = (VELOCIDAD_LUZ / (4 * np.pi * f_hz)) * (10 ** (tabla["l_trayecto_db"] / 20.0)) / 1000.0

    tabla_ordenada = tabla.sort_values(by="l_trayecto_db", ascending=False)

    print("--- Ranking de Enlaces por Pérdida de Trayecto ---")
    print(np.round(tabla_ordenada, 2))


if __name__ == "__main__":
    main()