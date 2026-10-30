"""Módulo de organización y asignación óptima de canales WiFi en 2.4 GHz."""

import numpy as np

CANALES_RECOMENDADOS = np.array([1, 6, 11])


def main():
    """Analiza y corrige los canales superpuestos de puntos de acceso."""
    canales = np.array([1, 6, 3, 11, 6, 9, 1, 11, 4, 6, 1, 13])

    # 1. Frecuencias centrales
    frecuencias_mhz = 2407 + (5 * canales)

    # 2. Canales recomendados
    en_recomendados = np.isin(canales, CANALES_RECOMENDADOS)
    cantidad_ok = np.sum(en_recomendados)
    cantidad_fuera = np.sum(~en_recomendados)

    # 3. Asignación al canal recomendado más cercano
    canales_corregidos = np.copy(canales)
    for i in range(len(canales)):
        if not en_recomendados[i]:
            diferencias = np.abs(CANALES_RECOMENDADOS - canales[i])
            canales_corregidos[i] = CANALES_RECOMENDADOS[np.argmin(diferencias)]

    print(f"Frecuencias centrales [MHz]: {frecuencias_mhz}")
    print(f"Puntos de acceso en canales recomendados: {cantidad_ok}")
    print(f"Puntos de acceso fuera de recomendación: {cantidad_fuera}")

    # 4. Distribución posterior
    print("\nDistribución corregida de APs por canal:")
    for c in CANALES_RECOMENDADOS:
        conteo = np.sum(canales_corregidos == c)
        print(f"Canal {c:<2}: {conteo} APs")


if __name__ == "__main__":
    main()