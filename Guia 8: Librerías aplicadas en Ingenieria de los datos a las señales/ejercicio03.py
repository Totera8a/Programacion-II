"""Módulo para decodificación espectral de tonos DTMF ruidosos."""

import numpy as np
from scipy.fft import fft, fftfreq

# Diccionarios invertidos para búsqueda rápida de frecuencias centrales
FREC_FILA = {697: '123', 770: '456', 852: '789', 941: '*0#'}
FREC_COLUMNA = {1209: '147*', 1336: '2580', 1477: '369#'}


def espectro(senal, fs):
    """Analizador de espectro por software (Cátedra)."""
    n = len(senal)
    amplitudes = 2 * np.abs(fft(senal))[:n // 2] / n
    frecuencias = fftfreq(n, 1 / fs)[:n // 2]
    return frecuencias, amplitudes


def decodificar_tecla(senal, fs):
    """Identifica la tecla DTMF procesando picos de frecuencia en la señal.

    Parámetros:
    senal -- Vector NumPy de la señal ruidosa.
    fs -- Frecuencia de muestreo.

    Retorna:
    Carácter correspondiente a la tecla decodificada (str).
    """
    frecuencias, amplitudes = espectro(senal, fs)

    # 2. Búsqueda con máscaras
    mask_fila = (frecuencias >= 650) & (frecuencias <= 1000)
    mask_col = (frecuencias >= 1150) & (frecuencias <= 1550)

    f_pico_fila = frecuencias[mask_fila][np.argmax(amplitudes[mask_fila])]
    f_pico_col = frecuencias[mask_col][np.argmax(amplitudes[mask_col])]

    # 3. Frecuencia más cercana de la tabla
    f_fila_real = min(FREC_FILA.keys(), key=lambda k: abs(k - f_pico_fila))
    f_col_real = min(FREC_COLUMNA.keys(), key=lambda k: abs(k - f_pico_col))

    # 4. Intersección para decodificar
    teclas_posibles_fila = set(FREC_FILA[f_fila_real])
    teclas_posibles_col = set(FREC_COLUMNA[f_col_real])
    tecla_decodificada = list(teclas_posibles_fila & teclas_posibles_col)[0]
    
    return tecla_decodificada


def main():
    """Genera tecla con ruido y prueba el decodificador."""
    fs = 8000.0
    duracion = 0.1
    t = np.arange(0, duracion, 1 / fs)
    rng = np.random.default_rng(3)

    # Señal de tecla 8 limpia + ruido
    tecla_8_limpia = np.sin(2 * np.pi * 852 * t) + np.sin(2 * np.pi * 1336 * t)
    ruido = rng.normal(0, 0.8, len(t))
    senal_rx = tecla_8_limpia + ruido

    tecla_detectada = decodificar_tecla(senal_rx, fs)
    print(f"Se esperaba la tecla 8. Se detectó: {tecla_detectada}")

    # Respuestas teóricas
    resolucion = fs / len(t)
    print(f"\nResolución en frecuencia: {resolucion:.1f} Hz")
    print("No hace falta que el pico caiga exactamente en el valor teórico porque la resolución")
    print("es discreta y elegimos el valor de tabla 'más cercano'.")


if __name__ == "__main__":
    main()