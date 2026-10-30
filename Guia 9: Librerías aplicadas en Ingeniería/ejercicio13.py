"""Módulo de regresión lineal para detección predictiva de degradación de señal."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    """Calcula la pendiente de degradación del RSSI y alerta sobre caídas lentas."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])
    pendientes = {}

    for estacion, grupo in df.dropna(subset=["rssi"]).groupby("estacion"):
        # 1. Calcular días transcurridos desde el primer reporte
        x_dias = (grupo["timestamp"] - grupo["timestamp"].min()).dt.total_seconds() / 86400.0
        y_rssi = grupo["rssi"]
        
        # 2. Regresión lineal (grado 1)
        coeficientes = np.polyfit(x_dias, y_rssi, 1)
        pendientes[estacion] = coeficientes[0]  # La pendiente es el primer coeficiente

    df_pendientes = pd.Series(pendientes)
    
    # 3. Marcar estaciones en degradación
    en_degradacion = df_pendientes[df_pendientes < -1.0]

    print("--- Estaciones EN DEGRADACIÓN (< -1 dB/día) ---")
    print(en_degradacion)

    print("\n--- Análisis Conceptual ---")
    positivas = df_pendientes[df_pendientes > 0].index.tolist()
    print(f"Estaciones con pendiente positiva: {positivas}")
    print("Una pendiente de ±0.05 dB/día no es preocupante; representa oscilaciones térmicas normales.")

    # 4. Gráfico de la estación detectada (E07)
    if not en_degradacion.empty:
        est_prob = en_degradacion.index[0]
        datos_est = df[(df["estacion"] == est_prob)].dropna(subset=["rssi"])
        x_graf = (datos_est["timestamp"] - datos_est["timestamp"].min()).dt.total_seconds() / 86400.0
        y_graf = datos_est["rssi"]
        p, b = np.polyfit(x_graf, y_graf, 1)

        plt.figure(figsize=(9, 5))
        plt.scatter(datos_est["timestamp"], y_graf, alpha=0.5, label="Mediciones RSSI", color="gray")
        plt.plot(datos_est["timestamp"], p * x_graf + b, color="red", linewidth=2, label=f"Ajuste ({p:.2f} dB/día)")
        plt.title(f"Degradación del Enlace: Estación {est_prob}")
        plt.xlabel("Fecha")
        plt.ylabel("RSSI [dBm]")
        plt.grid(True)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main()