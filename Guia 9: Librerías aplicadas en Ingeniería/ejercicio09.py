"""Módulo para la exportación de reportes en dialectos estándar e hispanos (CSV)."""

import numpy as np
import pandas as pd


def promedio_potencia_dbm(serie_rssi):
    """Calcula el promedio en potencia en dBm."""
    serie_valida = serie_rssi.dropna()
    potencia_mw = 10 ** (serie_valida / 10)
    return 10 * np.log10(potencia_mw.mean())


def main():
    """Genera, guarda e importa reportes tabulares validando la integridad."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Construir tabla resumen
    resumen = df.groupby("estacion").agg(
        banda=("frecuencia", "first"),
        rssi_promedio=("rssi", promedio_potencia_dbm),
        rssi_minimo=("rssi", "min"),
        alarmas_rssi=("rssi", lambda x: (x < -75.0).sum()),
        temp_maxima=("temperatura", "max"),
    ).round(2)

    # 2. Guardar estándar coma
    resumen.to_csv("resumen_red.csv")

    # 3. Guardar formato español punto y coma
    resumen.to_csv("resumen_red_es.csv", sep=";")

    # 4. Lectura e inspección
    df_coma = pd.read_csv("resumen_red.csv", index_col="estacion")
    df_punto_coma = pd.read_csv("resumen_red_es.csv", sep=";", index_col="estacion")

    print(f"¿Los archivos generados son idénticos?: {df_coma.equals(df_punto_coma)}")


if __name__ == "__main__":
    main()