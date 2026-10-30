"""Módulo para el cálculo del ancho de banda ocupado de señales moduladas y cuadradas."""

import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def generar_am(t, fc, fm, m):
    """Genera señal AM (del Ejercicio 9)."""
    return (1 + (m * np.cos(2 * np.pi * fm * t))) * np.cos(2 * np.pi * fc * t)


def onda_cuadrada(t, f0, cantidad_armonicos):
    """Genera aproximación de onda cuadrada (del Ejercicio 7)."""
    senal = np.zeros_like(t)
    for i in range(cantidad_armonicos):
        k = 2 * i + 1
        senal += (4 / (np.pi * k)) * np.sin(2 * np.pi * k * f0 * t)
    return senal


def ancho_banda_ocupado(frecuencias, amplitudes, fraccion):
    """Estima el ancho de banda donde la señal tiene energía significativa.

    Parámetros:
    frecuencias -- Vector de frecuencias del espectro.
    amplitudes -- Vector de amplitudes del espectro.
    fraccion -- Porcentaje respecto del pico máximo (ej. 0.01 para 1%).

    Retorna:
    Ancho de banda en Hz (float).
    """
    umbral = np.max(amplitudes) * fraccion
    mask = amplitudes > umbral
    frecs_validas = frecuencias[mask]
    
    if len(frecs_validas) == 0:
        return 0.0
    return frecs_validas[-1] - frecs_validas[0]


def main():
    """Analiza el ancho de banda ocupado por señales AM y ondas cuadradas."""
    fs = 20000.0
    t = np.arange(0, 1.0, 1 / fs)

    # 1. Señal AM variando fm
    print("--- Ancho de Banda Ocupado: Modulación AM (fc = 1000 Hz) ---")
    for fm in [50.0, 100.0, 200.0]:
        am = generar_am(t, 1000.0, fm, 0.5)
        frec, amp = espectro(am, fs)
        bw = ancho_banda_ocupado(frec, amp, 0.01)
        print(f"fm = {fm:<5.0f} Hz -> Ancho de Banda = {bw:.1f} Hz (Equivale a 2 * fm)")

    # 2. Onda Cuadrada variando armónicos
    print("\n--- Ancho de Banda Ocupado: Onda Cuadrada (f0 = 100 Hz) ---")
    for k in [1, 10, 50]:
        cuadrada = onda_cuadrada(t, 100.0, k)
        frec, amp = espectro(cuadrada, fs)
        bw = ancho_banda_ocupado(frec, amp, 0.01)
        print(f"Armónicos = {k:<2} -> Ancho de Banda = {bw:.1f} Hz")

    print("\n--- Conclusión Onda Cuadrada ---")
    print("Una onda cuadrada perfecta requiere tiempos de subida nulos, lo que matemáticamente")
    print("implica infinitos armónicos y, por lo tanto, un ancho de banda infinito.")


if __name__ == "__main__":
    main()