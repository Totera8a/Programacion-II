"""Módulo para generación y análisis de tonos telefónicos DTMF."""

import matplotlib.pyplot as plt
import numpy as np

# Diccionarios de frecuencias [Hz]
FILAS = {1: 697, 2: 697, 3: 697, 4: 770, 5: 770, 6: 770, 7: 852, 8: 852, 9: 852, '*': 941, 0: 941, '#': 941}
COLUMNAS = {1: 1209, 2: 1336, 3: 1477, 4: 1209, 5: 1336, 6: 1477, 7: 1209, 8: 1336, 9: 1477, '*': 1209, 0: 1336, '#': 1477}


def tono_dtmf(tecla, tiempos):
    """Genera la señal correspondiente a una tecla DTMF.

    Parámetros:
    tecla -- Carácter o entero correspondiente a la tecla.
    tiempos -- Vector NumPy de instantes de tiempo.

    Retorna:
    Señal DTMF en el tiempo (ndarray).
    """
    f_fila = FILAS[tecla]
    f_col = COLUMNAS[tecla]
    tono_fila = np.sin(2 * np.pi * f_fila * tiempos)
    tono_columna = np.sin(2 * np.pi * f_col * tiempos)
    return tono_fila + tono_columna


def cumple_nyquist(fs, frecuencias):
    """Verifica si la frecuencia de muestreo cumple el teorema de Nyquist."""
    f_max = max(frecuencias)
    return fs > 2 * f_max


def main():
    """Genera tonos DTMF, verifica Nyquist y grafica las formas de onda."""
    fs = 8000.0
    duracion = 0.1
    t = np.arange(0, duracion, 1 / fs)

    # Generar tecla 5
    tecla_5 = tono_dtmf(5, t)

    # Verificación de Nyquist
    todas_frecuencias = list(FILAS.values()) + list(COLUMNAS.values())
    cumple = cumple_nyquist(fs, todas_frecuencias)
    print(f"¿Fs={fs} Hz cumple Nyquist para DTMF?: {cumple}")

    # Graficar primeros 20 ms de teclas 1 y 9
    t_20ms = t[t <= 0.02]
    tecla_1 = tono_dtmf(1, t_20ms)
    tecla_9 = tono_dtmf(9, t_20ms)

    plt.figure(figsize=(8, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(t_20ms * 1000, tecla_1, color="blue")
    plt.title("Tecla 1 - Primeros 20 ms")
    plt.ylabel("Amplitud")
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t_20ms * 1000, tecla_9, color="orange")
    plt.title("Tecla 9 - Primeros 20 ms")
    plt.xlabel("Tiempo [ms]")
    plt.ylabel("Amplitud")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()