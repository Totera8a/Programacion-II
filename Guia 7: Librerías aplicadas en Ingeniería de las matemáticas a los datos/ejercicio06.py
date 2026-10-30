"""Módulo de verificación de ganancia acumulada en escala logarítmica y lineal."""

import math


def main():
    """Calcula la potencia de salida por suma de dB y multiplicación escalar."""
    p_entrada_dbm = -90.0
    etapas = [
        ("Cable de antena", -2.5),
        ("LNA", 20.0),
        ("Filtro", -1.5),
        ("Mezclador", -7.0),
        ("Amplificador FI", 30.0),
    ]

    # Cálculo paso a paso en dBm
    p_dbm_actual = p_entrada_dbm
    print("--- Progreso en Escala Logarítmica (dBm) ---")
    for nombre, g_db in etapas:
        p_dbm_actual += g_db
        print(f"Salida {nombre:<25}: {p_dbm_actual:.2f} dBm")

    # Cálculo paso a paso en escala lineal (mW)
    p_mw_actual = 10 ** (p_entrada_dbm / 10)
    print("\n--- Progreso en Escala Lineal (mW -> dBm) ---")
    for nombre, g_db in etapas:
        ganancia_lineal = 10 ** (g_db / 10)
        p_mw_actual *= ganancia_lineal
        p_dbm_convertida = 10 * math.log10(p_mw_actual)
        print(f"Salida {nombre:<25}: {p_dbm_convertida:.2f} dBm")

    # Verificación final
    son_iguales = math.isclose(p_dbm_actual, 10 * math.log10(p_mw_actual))
    print(f"\n¿Coinciden ambos métodos de cálculo?: {son_iguales}")


if __name__ == "__main__":
    main()