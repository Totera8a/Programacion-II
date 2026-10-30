"""Módulo de análisis de anomalías relativas mediante mediana móvil de la red."""

import pandas as pd


def main():
    """Determina qué estación sufrió un cambio de desempeño relativo mayor."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1 y 2. Mediana instantánea de la red y diferencia
    mediana_instantanea = df.groupby("timestamp")["rssi"].transform("median")
    df["diferencia_mediana"] = df["rssi"] - mediana_instantanea

    # 3. Promedio al inicio (5-6 Oct) y al final (10-11 Oct)
    df_inicio = df[df["timestamp"].dt.day.isin([5, 6])]
    df_fin = df[df["timestamp"].dt.day.isin([10, 11])]

    prom_inicio = df_inicio.groupby("estacion")["diferencia_mediana"].mean()
    prom_fin = df_fin.groupby("estacion")["diferencia_mediana"].mean()

    # 4. Variación de posición relativa
    variacion_relativa = (prom_fin - prom_inicio).abs().sort_values(ascending=False)

    print("--- Variación Absoluta de Posición Relativa respecto a la Red ---")
    print(variacion_relativa.round(2))
    print(f"\nLa estación que más cambió su comportamiento relativo fue: {variacion_relativa.idxmax()}")


if __name__ == "__main__":
    main()