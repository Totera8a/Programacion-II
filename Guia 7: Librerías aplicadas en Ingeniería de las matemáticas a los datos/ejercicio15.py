"""Módulo de gráficos semilogarítmicos de FSPL e incremento por década."""

import matplotlib.pyplot as plt
import numpy as np

VELOCIDAD_LUZ = 299792458


def main():
    """Grafica FSPL vs. distancia logarítmica y calcula distancia para 120 dB de pérdida."""
    distancias_m = np.logspace(1, 5, 1000)  # De 10 m a 100 km
    frecuencias = [
        ("433 MHz", 433e6),
        ("900 MHz", 900e6),
        ("2.4 GHz", 2.4e9),
        ("5.8 GHz", 5.8e9),
    ]

    plt.figure(figsize=(10, 6))

    print(f"{'Frecuencia':<12} | {'Distancia para 120 dB de FSPL [km]':<35}")
    print("-" * 52)

    for nombre, f_hz in frecuencias:
        fspl = 20 * np.log10((4 * np.pi * distancias_m * f_hz) / VELOCIDAD_LUZ)
        plt.semilogx(distancias_m, fspl, label=nombre)

        # Despeje: d = (10^(FSPL/20) * c) / (4 * pi * f)
        d_120_m = (10 ** (120.0 / 20.0) * VELOCIDAD_LUZ) / (4 * np.pi * f_hz)
        print(f"{nombre:<12} | {d_120_m / 1000.0:<35.2f}")

    plt.axhline(y=120.0, color="red", linestyle="--", label="Límite 120 dB")
    plt.title("Pérdida en Espacio Libre vs. Distancia (Escala Logarítmica)")
    plt.xlabel("Distancia [m]")
    plt.ylabel("FSPL [dB]")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Pendiente ---")
    print("La pendiente de todas las rectas en escala logarítmica es de 20 dB por década.")


if __name__ == "__main__":
    main()