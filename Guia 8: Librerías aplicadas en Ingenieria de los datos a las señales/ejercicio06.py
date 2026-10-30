"""Módulo de evaluación de interferencias por desplazamiento de fase."""

import matplotlib.pyplot as plt
import numpy as np


def retardo_us(fase_rad, frecuencia_hz):
    """Calcula el retardo temporal en microsegundos correspondiente a una fase."""
    retardo_segundos = fase_rad / (2 * np.pi * frecuencia_hz)
    return retardo_segundos * 1e6


def main():
    """Genera señales desfasadas y comprueba la interferencia destructiva."""
    fs = 100000.0
    frecuencia = 1000.0
    t = np.arange(0, 0.005, 1 / fs)  # 5 ms

    senal_directa = np.sin(2 * np.pi * frecuencia * t)
    fases = [np.pi / 2, np.pi, 3 * np.pi / 2]
    nombres_fases = ["pi/2", "pi", "3pi/2"]

    plt.figure(figsize=(12, 4))

    for i, fase in enumerate(fases):
        retardo = retardo_us(fase, frecuencia)
        senal_reflejada = np.sin(2 * np.pi * frecuencia * t + fase)
        senal_suma = senal_directa + senal_reflejada
        amp_suma = np.max(np.abs(senal_suma))

        print(f"Fase: {nombres_fases[i]:<6} | Retardo: {retardo:5.0f} us | Amplitud Suma: {amp_suma:.2f}")

        # Gráfico (solo primeros 2 ms)
        t_2ms = t <= 0.002
        plt.subplot(1, 3, i + 1)
        plt.plot(t[t_2ms] * 1000, senal_directa[t_2ms], label="Directa")
        plt.plot(t[t_2ms] * 1000, senal_reflejada[t_2ms], label="Reflejada", linestyle="--")
        plt.plot(t[t_2ms] * 1000, senal_suma[t_2ms], label="Suma", color="black", linewidth=2)
        plt.title(f"Fase: {nombres_fases[i]}")
        plt.xlabel("Tiempo [ms]")
        if i == 0:
            plt.ylabel("Amplitud")
        plt.grid(True)
        plt.legend()

    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("Con la fase igual a pi, la amplitud de la suma se vuelve nula (interferencia destructiva).")


if __name__ == "__main__":
    main()