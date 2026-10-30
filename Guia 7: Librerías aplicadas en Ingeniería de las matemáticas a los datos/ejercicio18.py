"""Módulo para el cálculo de patrones de radiación y ancho de haz a -3 dB."""

import matplotlib.pyplot as plt
import numpy as np

GANANCIA_MAX_DBI = 15.0


def main():
    """Grafica el diagrama de radiación para distintos factores de directividad n."""
    theta_deg = np.arange(-89.0, 89.1, 0.1)
    theta_rad = np.radians(theta_deg)
    directividades = [2, 10, 50]

    plt.figure(figsize=(9, 6))

    print(f"{'Directividad n':<15} | {'Ancho Haz Mscara [deg]':<25} | {'Ancho Haz Exacto [deg]':<25}")
    print("-" * 70)

    for n in directividades:
        # Modelo de radiación
        g_theta = GANANCIA_MAX_DBI + (10 * np.log10(np.cos(theta_rad) ** n))
        plt.plot(theta_deg, g_theta, label=f"n = {n}")

        # Ancho de haz con máscara de NumPy
        mascara_3db = g_theta >= (GANANCIA_MAX_DBI - 3.0)
        angulos_3db = theta_deg[mascara_3db]
        ancho_num = angulos_3db[-1] - angulos_3db[0]

        # Ancho de haz exacto
        ancho_exacto = np.degrees(2 * np.arccos(0.5 ** (1.0 / n)))

        print(f"{n:<15} | {ancho_num:<25.2f} | {ancho_exacto:<25.2f}")

    plt.title("Diagrama de Radiación (G_max = 15 dBi)")
    plt.xlabel("Ángulo θ [grados]")
    plt.ylabel("Ganancia G(θ) [dBi]")
    plt.ylim(0, 16)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("\n--- Conclusión ---")
    print("A mayor valor de n, la energía se concentra más en el eje principal, reduciendo el ancho de haz.")


if __name__ == "__main__":
    main()