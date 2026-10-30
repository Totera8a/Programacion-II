"""Módulo para el cálculo de piso de ruido térmico y SNR según el ancho de banda."""

import math

K_BOLTZMANN = 1.380649e-23
TEMPERATURA_K = 290.0
FIGURA_RUIDO_DB = 6.0
P_RX_DBM = -70.0


def main():
    """Calcula piso de ruido y SNR para distintos anchos de banda."""
    anchos_banda = [
        ("GSM (200 kHz)", 200e3),
        ("3G (5 MHz)", 5e6),
        ("WiFi (20 MHz)", 20e6),
        ("WiFi (80 MHz)", 80e6),
    ]

    print(f"{'Sistema':<18} | {'Ancho Banda [Hz]':<18} | {'Piso Ruido [dBm]':<18} | {'SNR [dB]':<10}")
    print("-" * 72)

    for sistema, b_hz in anchos_banda:
        # N[dBm] = 10*log10(k * T * B * 1000) + NF
        piso_ruido = 10 * math.log10(K_BOLTZMANN * TEMPERATURA_K * b_hz * 1000.0) + FIGURA_RUIDO_DB
        snr = P_RX_DBM - piso_ruido
        print(f"{sistema:<18} | {b_hz:<18.0f} | {piso_ruido:<18.2f} | {snr:<10.2f}")

    print("\n--- Conclusión ---")
    print("Al aumentar el ancho de banda, el piso de ruido crece proporcionalmente, lo que reduce la SNR.")


if __name__ == "__main__":
    main()