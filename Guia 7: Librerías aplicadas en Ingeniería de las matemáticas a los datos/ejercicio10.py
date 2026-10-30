"""Módulo para el cálculo de capacidad teórica de Shannon-Hartley."""

import math


def capacidad_shannon(ancho_banda_hz, snr_db):
    """Calcula la capacidad de Shannon en bits/segundo.

    Parámetros:
    ancho_banda_hz -- Ancho de banda en Hertz.
    snr_db -- Relación señal a ruido en dB.

    Retorna:
    Capacidad en bit/s (float).
    """
    snr_lineal = 10 ** (snr_db / 10)
    return ancho_banda_hz * math.log2(1 + snr_lineal)


def main():
    """Analiza la capacidad al variar ancho de banda versus SNR."""
    # Parte 1: Variando ancho de banda con SNR fija de 25 dB
    print("--- Capacidad variando Ancho de Banda (SNR = 25 dB) ---")
    anchos_mhz = [20, 40, 80, 160]
    for b in anchos_mhz:
        cap = capacidad_shannon(b * 1e6, 25.0) / 1e6
        print(f"B = {b:<3} MHz -> Capacidad = {cap:.2f} Mbit/s")

    # Parte 2: Variando SNR con ancho de banda fijo de 20 MHz
    print("\n--- Capacidad variando SNR (B = 20 MHz) ---")
    snrs = [0, 5, 10, 20, 30]
    for snr in snrs:
        cap = capacidad_shannon(20e6, snr) / 1e6
        print(f"SNR = {snr:<2} dB -> Capacidad = {cap:.2f} Mbit/s")

    print("\n--- Justificación ---")
    print("Conviene duplicar el ancho de banda. La capacidad escala de forma LINEAL con B,")
    print("mientras que escalar con la SNR sigue una relación LOGARÍTMICA de menor rendimiento.")


if __name__ == "__main__":
    main()