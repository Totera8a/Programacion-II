"""Módulo de serialización y segmentación para decodificar cadenas DTMF enteras."""

import numpy as np
from scipy.fft import fft, fftfreq

# Diccionarios de frecuencias [Hz]
FILAS = {1: 697, 2: 697, 3: 697, 4: 770, 5: 770, 6: 770, 7: 852, 8: 852, 9: 852, '*': 941, 0: 941, '#': 941}
COLUMNAS = {1: 1209, 2: 1336, 3: 1477, 4: 1209, 5: 1336, 6: 1477, 7: 1209, 8: 1336, 9: 1477, '*': 1209, 0: 1336, '#': 1477}
FREC_FILA = {697: '123', 770: '456', 852: '789', 941: '*0#'}
FREC_COLUMNA = {1209: '147*', 1336: '2580', 1477: '369#'}


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def generar_marcacion(numero, fs, rng):
    """Construye la señal de una secuencia telefónica.

    Parámetros:
    numero -- Secuencia de dígitos como cadena o entero.
    fs -- Frecuencia de muestreo.
    rng -- Generador de números aleatorios para inyección de ruido.

    Retorna:
    Señal DTMF seriada contaminada con ruido Gaussiano.
    """
    t_tono = np.arange(0, 0.1, 1 / fs)
    silencio = np.zeros(int(0.05 * fs))
    tramos = []

    for d in str(numero):
        d_int = int(d)
        tono = np.sin(2 * np.pi * FILAS[d_int] * t_tono) + np.sin(2 * np.pi * COLUMNAS[d_int] * t_tono)
        tramos.append(tono)
        tramos.append(silencio)

    # Quitar el último silencio y concatenar
    senal_limpia = np.concatenate(tramos[:-1])
    ruido = rng.normal(0, 0.5, len(senal_limpia))
    return senal_limpia + ruido


def decodificar_tecla(senal, fs):
    """Identifica la tecla de un pulso ruidoso (del Ejercicio 3)."""
    frec, amp = espectro(senal, fs)
    
    mask_fila = (frec >= 650) & (frec <= 1000)
    mask_col = (frec >= 1150) & (frec <= 1550)

    f_pico_fila = frec[mask_fila][np.argmax(amp[mask_fila])]
    f_pico_col = frec[mask_col][np.argmax(amp[mask_col])]

    f_fila_real = min(FREC_FILA.keys(), key=lambda k: abs(k - f_pico_fila))
    f_col_real = min(FREC_COLUMNA.keys(), key=lambda k: abs(k - f_pico_col))

    teclas_posibles_fila = set(FREC_FILA[f_fila_real])
    teclas_posibles_col = set(FREC_COLUMNA[f_col_real])
    
    return list(teclas_posibles_fila & teclas_posibles_col)[0]


def segmentar(senal, fs):
    """Corta la señal en tramos asumiendo periodos fijos (0.1s pulso + 0.05s silencio)."""
    largo_pulso = int(0.1 * fs)
    largo_bloque = int(0.15 * fs)
    teclas_detectadas = ""
    
    i = 0
    while i < len(senal):
        tramo_tecla = senal[i:i + largo_pulso]
        if len(tramo_tecla) == largo_pulso:
            teclas_detectadas += decodificar_tecla(tramo_tecla, fs)
        i += largo_bloque

    return teclas_detectadas


def main():
    """Simula y decodifica las llamadas completas ingresadas."""
    fs = 8000.0
    rng = np.random.default_rng(19)

    numeros_a_probar = ["35812", "90467"]

    for n_original in numeros_a_probar:
        senal = generar_marcacion(n_original, fs, rng)
        n_detectado = segmentar(senal, fs)
        print(f"Marcado original: {n_original} | Detección: {n_detectado}")


if __name__ == "__main__":
    main()