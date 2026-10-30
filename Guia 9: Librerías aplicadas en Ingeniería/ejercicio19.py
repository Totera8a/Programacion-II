"""Módulo de modelado predictivo para el corte de servicio por degradación."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    """Interpola linealmente la caída de señal para advertir fecha de desconexión."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Filtrar estación E07 a partir del inicio de la falla (ej. 7 de octubre)
    df_e07 = df[(df["estacion"] == "E07") & (df["timestamp"] >= "2026-10-07")].dropna(subset=["rssi"])
    t0 = pd.Timestamp("2026-10-05 00:00:00")
    
    x_dias = (df_e07["timestamp"] - t0).dt.total_seconds() / 86400.0
    y_rssi = df_e07["rssi"]

    # 2. Recta de ajuste
    p, b = np.polyfit(x_dias, y_rssi, 1)

    # 3. Despeje de X para y = -85 dBm -> x = (-85 - b) / p
    x_corte = (-85.0 - b) / p
    fecha_corte = t0 + pd.Timedelta(days=x_corte)

    print(f"Tasa de degradación: {p:.2f} dB/día")
    print(f"Fecha estimada de corte de enlace (-85 dBm): {fecha_corte.strftime('%Y-%m-%d %H:%M:%S')}")

    # 4. Gráfico extendido
    x_proy = np.linspace(x_dias.min(), x_corte + 1, 100)
    fechas_proy = [t0 + pd.Timedelta(days=val) for val in x_proy]
    y_proy = p * x_proy + b

    plt.figure(figsize=(10, 5))
    plt.scatter(df_e07["timestamp"], y_rssi, alpha=0.5, label="Datos Históricos")
    plt.plot(fechas_proy, y_proy, color="red", linestyle="--", label="Proyección Lineal")
    plt.axhline(y=-75.0, color="orange", linestyle=":", label="Alarma (-75 dBm)")
    plt.axhline(y=-85.0, color="black", linestyle="-.", label="Corte Total (-85 dBm)")

    plt.title("Proyección de Vida Útil Restante del Enlace E07")
    plt.xlabel("Fecha")
    plt.ylabel("RSSI [dBm]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Confiabilidad Predictiva ---")
    print("La predicción puede fallar dramáticamente por dos motivos fundamentales:")
    print("1. El comportamiento de los componentes físicos raramente es lineal en el colapso final.")
    print("2. Un evento meteorológico externo podría superponer atenuación destruyendo la tendencia.")


if __name__ == "__main__":
    main()