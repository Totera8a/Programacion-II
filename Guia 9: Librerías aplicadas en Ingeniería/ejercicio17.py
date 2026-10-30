"""Módulo de inyección de datos simulados y expansión del DataFrame de telemetría."""

import numpy as np
import pandas as pd


def main():
    """Genera datos sintéticos para E21 y los anexa a la telemetría histórica."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Crear marcas de tiempo
    fechas = pd.date_range(start="2026-10-05 00:00:00", periods=672, freq="15min")

    # 2. Simular RSSI y Temperatura
    rng = np.random.default_rng(21)
    rssi_sim = rng.normal(-66.0, 1.5, len(fechas))
    
    horas = fechas.hour.values
    temp_teorica = 25.0 + 7.0 * np.sin((2 * np.pi * (horas - 9)) / 24.0)
    temp_sim = temp_teorica + rng.normal(0, 0.8, len(fechas))

    # 3. Armar DataFrame y concatenar
    df_e21 = pd.DataFrame({
        "timestamp": fechas,
        "estacion": "E21",
        "frecuencia": 2400,
        "potencia": 23,
        "rssi": rssi_sim,
        "temperatura": temp_sim
    })

    df_ampliado = pd.concat([df, df_e21], ignore_index=True)

    # 4. Verificación
    print("--- Verificación de Integración de E21 ---")
    print(f"Total de registros ahora: {len(df_ampliado)} (Esperado: 14072)")
    print(f"Total de estaciones ahora: {df_ampliado['estacion'].nunique()} (Esperado: 21)")


if __name__ == "__main__":
    main()