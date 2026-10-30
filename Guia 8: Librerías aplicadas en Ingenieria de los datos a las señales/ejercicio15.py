"""Módulo de comprobación de retardos de fase en filtros causales vs bidireccionales."""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def main():
    """Aplica filtros en tiempo real y offline para evaluar el retardo temporal."""
    fs = 1000.0
    t = np.arange(0, 1.0, 1 / fs)

    # Pulso gaussiano
    pulso = np.exp(-(((t - 0.5) / 0.01) ** 2))
    idx_max_orig = np.argmax(pulso)
    t_max_orig = t[idx_max_orig]

    fc_pruebas = [30.0, 15.0, 60.0]
    
    plt.figure(figsize=(12, 4))

    for i, fc in enumerate(fc_pruebas):
        # 1. Filtrado
        b, a = signal.butter(4, fc, btype='lowpass', fs=fs)
        salida_filtfilt = signal.filtfilt(b, a, pulso)
        salida_lfilter = signal.lfilter(b, a, pulso)

        # 2. Retardos
        idx_ff = np.argmax(salida_filtfilt)
        idx_lf = np.argmax(salida_lfilter)

        retardo_ff_ms = (t[idx_ff] - t_max_orig) * 1000.0
        retardo_lf_ms = (t[idx_lf] - t_max_orig) * 1000.0

        print(f"fc = {fc:<4.0f} Hz -> Retardo filtfilt: {retardo_ff_ms:5.1f} ms | Retardo lfilter: {retardo_lf_ms:5.1f} ms")

        # 3. Gráficos (zoom 0.4s a 0.6s)
        mask_zoom = (t >= 0.4) & (t <= 0.6)
        plt.subplot(1, 3, i + 1)
        plt.plot(t[mask_zoom], pulso[mask_zoom], label="Original", color="gray", linestyle="--")
        plt.plot(t[mask_zoom], salida_filtfilt[mask_zoom], label="filtfilt (Fase 0)", color="green")
        plt.plot(t[mask_zoom], salida_lfilter[mask_zoom], label="lfilter (Causal)", color="red")
        plt.title(f"fc = {fc} Hz")
        plt.xlabel("Tiempo [s]")
        if i == 0:
            plt.ylabel("Amplitud")
        plt.grid(True)
        plt.legend(fontsize=8)

    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("El retardo de lfilter AUMENTA cuando se reduce la frecuencia de corte.")
    print("Un receptor en tiempo real NO puede usar filtfilt porque este necesita procesar")
    print("la señal 'hacia el futuro' (aplicación bidireccional sobre datos ya almacenados).")


if __name__ == "__main__":
    main()