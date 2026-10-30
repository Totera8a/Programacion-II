"""Módulo para el cálculo de distancia de visión directa sobre la curvatura terrestre."""

import math


def horizonte_km(h1_m, h2_m):
    """Calcula el horizonte de radio en kilómetros dadas las alturas de dos antenas.

    Parámetros:
    h1_m -- Altura de la primera antena en metros.
    h2_m -- Altura de la segunda antena en metros.

    Retorna:
    Distancia máxima de horizonte en km (float).
    """
    return 4.12 * (math.sqrt(h1_m) + math.sqrt(h2_m))


def main():
    """Calcula el horizonte de radio para distintas configuraciones de torres."""
    # Caso 1: Torre y vehículo
    d_auto = horizonte_km(30.0, 1.5)
    print(f"Horizonte Torre (30m) - Auto (1.5m): {d_auto:.2f} km")

    # Caso 2: Torres de igual altura
    alturas = [30.0, 45.0, 60.0]
    print("\nHorizonte entre torres de igual altura:")
    for h in alturas:
        print(f"Torres de {h:.0f}m - {h:.0f}m: {horizonte_km(h, h):.2f} km")

    # Despeje para d_max = 50 km con h1 = h2 = h
    # 50 = 4.12 * 2 * sqrt(h) => sqrt(h) = 50 / 8.24 => h = (50 / 8.24)**2
    h_minima = (50.0 / 8.24) ** 2
    print(f"\nAltura mínima requerida para enlace de 50 km (torres iguales): {h_minima:.2f} m")


if __name__ == "__main__":
    main()