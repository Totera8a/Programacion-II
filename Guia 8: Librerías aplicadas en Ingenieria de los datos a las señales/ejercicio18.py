"""Módulo de simulación de detección de portadoras piloto e índice de falsas alarmas."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def detecta_piloto(senal, fs, umbral):
    """Detecta la presencia del tono piloto de 19 kHz.

    Parámetros:
    senal -- Vector NumPy de la señal en banda base.
    fs -- Frecuencia de muestreo.
    umbral -- Umbral de detección espectral de amplitud.

    Retorna:
    Booleano indicando si el piloto está presente.
    """
    frec, amp = espectro(senal, fs)
    mask = (frec >= 18900.0) & (frec <= 19100.0)
    pico_maximo = np.max(amp[mask])
    return pico_maximo > umbral


def main():
    """Ejecuta simulación Monte Carlo para evaluar tasas de detección y falsas alarmas."""
    fs = 48000.0
    t = np.arange(0, 0.05, 1 / fs)
    umbral_fijo = 0.1
    
    amplitudes_piloto = [0.05, 0.1, 0.2, 0.4]
    tasas_deteccion = []

    print(f"Umbral estricto: {umbral_fijo}")
    
    # 2. Simular 50 recepciones para cada amplitud
    for a in amplitudes_piloto:
        exitos = 0
        for semilla in range(50):
            rng = np.random.default_rng(semilla)
            piloto = a * np.sin(2 * np.pi * 19000.0 * t)
            ruido = rng.normal(0, 1.0, len(t))
            rx = piloto + ruido
            
            if detecta_piloto(rx, fs, umbral_fijo):
                exitos += 1
                
        pct = (exitos / 50.0) * 100.0
        tasas_deteccion.append(pct)
        print(f"Amplitud = {a:<4} -> Detección: {pct:3.0f}%")

    # 3. Falsas alarmas (solo ruido)
    falsas = 0
    for semilla in range(50):
        rng = np.random.default_rng(semilla)
        rx_ruido = rng.normal(0, 1.0, len(t))
        if detecta_piloto(rx_ruido, fs, umbral_fijo):
            falsas += 1
    
    print(f"Falsas alarmas (solo ruido): {(falsas / 50.0) * 100.0:.0f}%")

    # 4. Gráfico
    plt.figure(figsize=(7, 4))
    plt.plot(amplitudes_piloto, tasas_deteccion, marker="s", color="green")
    plt.title(f"Tasa de Detección de Piloto FM (Umbral = {umbral_fijo})")
    plt.xlabel("Amplitud del Tono Piloto")
    plt.ylabel("Tasa de Detección Exitosa [%]")
    plt.grid(True)
    plt.show()

    print("\n--- Análisis de Compromiso ---")
    print("Si bajamos el umbral a 0.05, la sensibilidad aumenta y detectaremos más tonos débiles.")
    print("Sin embargo, los picos aleatorios de ruido cruzarán más fácilmente ese límite,")
    print("disparando dramáticamente el porcentaje de FALSAS ALARMAS (detectar estéreo cuando no lo hay).")


if __name__ == "__main__":
    main()