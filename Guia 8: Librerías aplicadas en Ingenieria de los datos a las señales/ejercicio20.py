"""Módulo integrador de análisis de espectro y generación de reportes automáticos."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def espectro_db(amplitudes):
    """Normaliza las amplitudes y convierte a dB respecto al máximo."""
    maximo = np.max(amplitudes)
    # np.maximum evita logaritmo de cero
    return 20 * np.log10(np.maximum(amplitudes / maximo, 1e-10))


def piso_ruido(amplitudes_db):
    """Calcula el piso de ruido como la mediana de las amplitudes en dB."""
    return np.median(amplitudes_db)


def picos(frecuencias, amplitudes_db, margen_db):
    """Encuentra picos espectrales por encima del piso de ruido + margen.

    Retorna:
    Tupla de listas: (frecuencias_pico, amplitudes_db_pico)
    """
    umbral = piso_ruido(amplitudes_db) + margen_db
    mask = amplitudes_db > umbral
    return frecuencias[mask], amplitudes_db[mask]


def ancho_banda_ocupado(frecuencias, amplitudes, fraccion):
    """Calcula BW basado en espectro lineal."""
    umbral = np.max(amplitudes) * fraccion
    mask = amplitudes > umbral
    frecs_validas = frecuencias[mask]
    if len(frecs_validas) == 0:
        return 0.0
    return frecs_validas[-1] - frecs_validas[0]


def informe(senal, fs, nombre):
    """Procesa la señal, imprime el diagnóstico integral y genera el gráfico."""
    frec, amp = espectro(senal, fs)
    amp_db = espectro_db(amp)

    pr_db = piso_ruido(amp_db)
    
    # Tolerancia de 20 dB por encima del piso para detectar picos
    f_picos, a_picos = picos(frec, amp_db, margen_db=20.0)

    frec_dominante = f_picos[np.argmax(a_picos)] if len(f_picos) > 0 else 0.0
    snr_pico = 0.0 - pr_db  # El máximo está normalizado a 0 dB
    
    bw = ancho_banda_ocupado(frec, amp, 0.01)

    print(f"\n=======================================================")
    print(f"      INFORME DE ANALIZADOR DE ESPECTRO: {nombre} ")
    print(f"=======================================================")
    print(f" - Frecuencia Dominante : {frec_dominante:.1f} Hz")
    print(f" - Piso de Ruido (Norm) : {pr_db:.2f} dB")
    print(f" - SNR Pico Dominante   : {snr_pico:.2f} dB")
    print(f" - Ancho de Banda (1%)  : {bw:.1f} Hz")
    print(f" - Lista de Picos Detectados (> Piso + 20dB):")
    for fp, ap in zip(f_picos, a_picos):
        print(f"      -> {fp:5.1f} Hz [{ap:6.2f} dB]")

    # Gráficos
    t = np.arange(0, len(senal)) / fs
    plt.figure(figsize=(12, 5))

    # Temporal (solo 20 ms iniciales)
    t_20ms = t <= 0.02
    plt.subplot(1, 2, 1)
    plt.plot(t[t_20ms] * 1000, senal[t_20ms], color="gray")
    plt.title(f"{nombre} - Temporal")
    plt.xlabel("Tiempo [ms]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Espectral en dB
    plt.subplot(1, 2, 2)
    plt.plot(frec, amp_db, color="blue")
    plt.axhline(y=pr_db + 20.0, color="red", linestyle="--", label="Umbral de Picos")
    plt.title("Espectro Normalizado")
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud Normalizada [dB]")
    plt.ylim(-100, 5)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    """Evalúa el analizador integrador contra tres señales complejas."""
    fs = 10000.0
    t = np.arange(0, 1.0, 1 / fs)

    # 1. DTMF Tecla 7 (852 Hz, 1209 Hz)
    rng_dtmf = np.random.default_rng(7)
    tecla_7 = np.sin(2 * np.pi * 852 * t) + np.sin(2 * np.pi * 1209 * t)
    tecla_7 += rng_dtmf.normal(0, 0.3, len(t))
    informe(tecla_7, fs, "DTMF Tecla 7")

    # 2. AM m=0.5
    rng_am = np.random.default_rng(9)
    am = (1 + (0.5 * np.cos(2 * np.pi * 50 * t))) * np.cos(2 * np.pi * 1000 * t)
    am += rng_am.normal(0, 0.1, len(t))
    informe(am, fs, "Modulación AM (m=0.5)")

    # 3. Señal misteriosa
    rng_mist = np.random.default_rng(4)
    # Replicamos interno de la función misteriosa para control
    frecuencias = rng_mist.choice(np.arange(500, 4500, 10), 3, replace=False)
    amplitudes = rng_mist.uniform(0.3, 1.0, 3)
    senal_mist = np.zeros(len(t))
    for f, a in zip(frecuencias, amplitudes):
        senal_mist += a * np.sin(2 * np.pi * f * t)
    senal_mist += rng_mist.normal(0, 0.8, len(t))
    informe(senal_mist, fs, "Señal Misteriosa")


if __name__ == "__main__":
    main()