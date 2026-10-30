"""Módulo de aislamiento e inspección cruzada de incidentes térmicos críticos."""

import matplotlib.pyplot as plt
import pandas as pd


def main():
    """Extrae el pico térmico de la semana y evalúa su impacto en el enlace."""
    df = pd.read_csv("telemetria.csv", parse_dates=["timestamp"])

    # 1. Buscar pico máximo absoluto
    idx_max = df["temperatura"].idxmax()
    registro_max = df.loc[idx_max]
    est_prob = registro_max["estacion"]
    hora_pico = registro_max["timestamp"]

    # 2. Extraer ventana de 6 horas
    ventana = df[
        (df["estacion"] == est_prob) & 
        (df["timestamp"] >= hora_pico - pd.Timedelta(hours=3)) & 
        (df["timestamp"] <= hora_pico + pd.Timedelta(hours=3))
    ]

    # 3. Duración del evento crítico
    muestras_criticas = (ventana["temperatura"] > 60.0).sum()
    duracion_minutos = muestras_criticas * 15

    # 4. Comparativa contra su estado habitual
    hora_del_dia = hora_pico.hour
    habitual = df[(df["estacion"] == est_prob) & (df["timestamp"].dt.hour == hora_del_dia)]["temperatura"].mean()
    sobre_habitual = registro_max["temperatura"] - habitual

    print(f"Estación afectada: {est_prob} | Pico: {registro_max['temperatura']} °C a las {hora_pico}")
    print(f"Duración del evento (> 60 °C): {duracion_minutos} minutos")
    print(f"Superó su media habitual ({habitual:.1f} °C) en {sobre_habitual:.1f} °C")

    # 5. Gráfico de doble eje / subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax1.plot(ventana["timestamp"], ventana["temperatura"], color="crimson", marker="o")
    ax1.axhline(y=60.0, color="orange", linestyle="--", label="Alarma (60 °C)")
    ax1.set_title(f"Evento Térmico Crítico en {est_prob}")
    ax1.set_ylabel("Temperatura [°C]")
    ax1.grid(True)
    ax1.legend()

    ax2.plot(ventana["timestamp"], ventana["rssi"], color="blue", marker="s")
    ax2.set_ylabel("RSSI [dBm]")
    ax2.set_xlabel("Hora")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

    print("\n¿El RSSI se vio afectado?: Viendo el gráfico correlacionado, se puede determinar")
    print("si la falla de temperatura degradó inmediatamente la circuitería del amplificador.")


if __name__ == "__main__":
    main()