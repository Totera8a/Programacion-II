"""Módulo de evaluación de despeje en la primera zona de Fresnel."""

import math


def radio_fresnel(d1_km, d2_km, frecuencia_ghz):
    """Calcula el radio de la primera zona de Fresnel en metros.

    Parámetros:
    d1_km -- Distancia a la primera antena en km.
    d2_km -- Distancia a la segunda antena en km.
    frecuencia_ghz -- Frecuencia del enlace en GHz.

    Retorna:
    Radio de Fresnel en metros (float).
    """
    d_total = d1_km + d2_km
    return 17.32 * math.sqrt((d1_km * d2_km) / (frecuencia_ghz * d_total))


def obstaculo_invade_fresnel(d1_km, d2_km, frecuencia_ghz, despeje_m):
    """Determina si un obstáculo invade más del 40% de la zona de Fresnel.

    Parámetros:
    d1_km -- Distancia a la primera antena en km.
    d2_km -- Distancia a la segunda antena en km.
    frecuencia_ghz -- Frecuencia del enlace en GHz.
    despeje_m -- Distancia del obstáculo a la línea de vista en metros.

    Retorna:
    True si la invasión supera el 40%, False en caso contrario.
    """
    r = radio_fresnel(d1_km, d2_km, frecuencia_ghz)
    invasion = (r - despeje_m) / r
    return invasion > 0.40


def main():
    """Evalúa la zona de Fresnel para un enlace de 10 km a 5.8 GHz."""
    frecuencia = 5.8
    # Punto medio de un enlace de 10 km
    r_medio = radio_fresnel(5.0, 5.0, frecuencia)
    print(f"Radio de Fresnel en el punto medio (5 km): {r_medio:.2f} m")

    # Obstáculo a 3 km (d1 = 3, d2 = 7) con despeje de 4 m
    d1, d2 = 3.0, 7.0
    despeje = 4.0
    r_obs = radio_fresnel(d1, d2, frecuencia)
    invade = obstaculo_invade_fresnel(d1, d2, frecuencia, despeje)

    porcentaje_invasion = ((r_obs - despeje) / r_obs) * 100
    print(f"Radio de Fresnel en el obstáculo (3 km): {r_obs:.2f} m")
    print(f"Invasión del obstáculo: {porcentaje_invasion:.1f}%")
    print(f"¿Invade más del 40%?: {invade}")


if __name__ == "__main__":
    main()