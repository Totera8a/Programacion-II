"""Módulo de caracterización térmica y detección de anomalías de temperatura."""

import pandas as pd


def main():
    """Genera rankings térmicos e identifica equipos expuestos a sobrecalentamiento."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Métricas por estación
    temp_stats = df.groupby("estacion")["temperatura"].agg(["min", "mean", "max"])

    # 2. Top 5 mayor temperatura máxima
    top5_max = temp_stats.sort_values(by="max", ascending=False).head(5)

    # 3. Amplitud térmica
    temp_stats["amplitud"] = temp_stats["max"] - temp_stats["min"]
    est_mayor_amplitud = temp_stats["amplitud"].idxmax()

    # 4. Estaciones sobre 35 °C
    sobre_35 = (df.groupby("estacion")["temperatura"].max() > 35.0).sum()

    print("--- Top 5 Estaciones con Mayor Temperatura Máxima ---")
    print(top5_max)
    print(f"\nEstación con mayor amplitud térmica: {est_mayor_amplitud} ({temp_stats.loc[est_mayor_amplitud, 'amplitud']:.1f} °C)")
    print(f"Estaciones que superaron los 35 °C al menos una vez: {sobre_35}")


if __name__ == "__main__":
    main()