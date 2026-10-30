"""Módulo de evaluación de caída (roll-off) en filtros de distintos órdenes."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    """Analiza la respuesta en frecuencia teórica de filtros Butterworth."""
    fs = 16000.0
    f_corte = 1000.0

    print(f"{'Orden':<8} | {'Atenuación a 2*fc (2000 Hz) [dB]':<35}")
    print("-" * 45)

    orden_minimo = None

    # 1. y 2. Calcular atenuación en 2fc para órdenes 1 a 10
    for orden in range(1, 11):
        b, a = signal.butter(orden, f_corte, btype='lowpass', fs=fs)
        frecuencias, h = signal.freqz(b, a, worN=4000, fs=fs)
        
        atenuacion_db = 20 * np.log10(np.abs(h))
        idx_2fc = np.argmin(np.abs(frecuencias - 2000.0))
        atenuacion_2fc = atenuacion_db[idx_2fc]
        
        print(f"{orden:<8} | {atenuacion_2fc:<35.2f}")

        # Capturar el primer orden que supere (sea más negativo que) -40 dB
        if atenuacion_2fc <= -40.0 and orden_minimo is None:
            orden_minimo = orden

    print(f"\nMenor orden necesario para atenuar al menos 40 dB en 2000 Hz: {orden_minimo}")

    # 3. Gráficos de respuesta
    plt.figure(figsize=(10, 6))

    for orden_graf in [2, 4, 8]:
        b, a = signal.butter(orden_graf, f_corte, btype='lowpass', fs=fs)
        frecuencias, h = signal.freqz(b, a, worN=4000, fs=fs)
        atenuacion_db = 20 * np.log10(np.abs(h))
        plt.plot(frecuencias, atenuacion_db, label=f"Orden {orden_graf}")

    plt.axvline(x=f_corte, color="red", linestyle=":", label="fc (1000 Hz)")
    plt.axvline(x=2000.0, color="purple", linestyle=":", label="2fc (2000 Hz)")
    plt.axhline(y=-3.0, color="gray", linestyle="--", label="-3 dB")

    plt.title("Respuesta en Frecuencia de Pasa-bajos Butterworth")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Ganancia [dB]")
    plt.xlim(0, 4000)
    plt.ylim(-80, 5)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()