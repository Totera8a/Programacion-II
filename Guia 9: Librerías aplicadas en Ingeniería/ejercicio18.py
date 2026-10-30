"""Módulo de construcción de dashboard general (Matplotlib) para el centro de operación."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def promedio_potencia_dbm(serie):
    """Calcula el promedio en potencia en dBm."""
    mw = 10 ** (serie.dropna() / 10)
    return 10 * np.log10(mw.mean())


def main():
    """Genera un tablero 2x2 resumiendo los KPIs de salud de la red."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))

    # --- 1. Arriba Izquierda: Margen promedio por estación ---
    rssi_prom = df.groupby("estacion")["rssi"].apply(promedio_potencia_dbm)
    margen = rssi_prom - (-75.0)
    colores = ["red" if m < 10.0 else "mediumseagreen" for m in margen]
    
    axs[0, 0].bar(margen.index, margen.values, color=colores)
    axs[0, 0].axhline(y=10.0, color="orange", linestyle="--")
    axs[0, 0].set_title("Margen Operativo Promedio por Estación")
    axs[0, 0].set_ylabel("Margen [dB]")
    axs[0, 0].tick_params(axis='x', rotation=45)

    # --- 2. Arriba Derecha: Alarmas por día ---
    df["fecha"] = df["timestamp"].dt.date
    alarmas_dia = df[df["rssi"] < -75.0].groupby("fecha").size()
    
    # Manejar días sin alarmas (para no romper la gráfica)
    dias_todos = df["fecha"].unique()
    alarmas_completas = alarmas_dia.reindex(dias_todos, fill_value=0)
    
    axs[0, 1].bar(alarmas_completas.index.astype(str), alarmas_completas.values, color="tomato")
    axs[0, 1].set_title("Alarmas Críticas de RSSI por Día")
    axs[0, 1].set_ylabel("Cantidad de Alarmas")
    axs[0, 1].tick_params(axis='x', rotation=45)

    # --- 3. Abajo Izquierda: RSSI de la peor estación ---
    estacion_peor = df[df["rssi"] < -75.0].groupby("estacion").size().idxmax()
    df_peor = df[df["estacion"] == estacion_peor].sort_values("timestamp")
    
    axs[1, 0].plot(df_peor["timestamp"], df_peor["rssi"], color="lightgray", label="Crudo")
    axs[1, 0].plot(df_peor["timestamp"], df_peor["rssi"].rolling(12).mean(), color="black", label="Media Móvil 3h")
    axs[1, 0].axhline(y=-75.0, color="red", linestyle=":", label="Umbral")
    axs[1, 0].set_title(f"Evolución RSSI - Estación Más Afectada ({estacion_peor})")
    axs[1, 0].set_ylabel("RSSI [dBm]")
    axs[1, 0].legend()
    axs[1, 0].tick_params(axis='x', rotation=45)

    # --- 4. Abajo Derecha: Perfil Térmico ---
    df["hora"] = df["timestamp"].dt.hour
    temp_red = df.groupby("hora")["temperatura"].mean()
    
    estacion_caliente = df.groupby("estacion")["temperatura"].max().idxmax()
    temp_caliente = df[df["estacion"] == estacion_caliente].groupby("hora")["temperatura"].mean()

    axs[1, 1].plot(temp_red.index, temp_red.values, color="blue", marker="o", label="Promedio Red")
    axs[1, 1].plot(temp_caliente.index, temp_caliente.values, color="red", marker="s", label=f"Peor Caso ({estacion_caliente})")
    axs[1, 1].axhline(y=60.0, color="orange", linestyle="--")
    axs[1, 1].set_title("Perfil Térmico Diario")
    axs[1, 1].set_xlabel("Hora del Día")
    axs[1, 1].set_ylabel("Temperatura [°C]")
    axs[1, 1].legend()

    plt.tight_layout()
    plt.savefig("tablero_red.png", dpi=150)
    print("Dashboard guardado exitosamente como 'tablero_red.png'")


if __name__ == "__main__":
    main()